import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "styles.css").read_text(encoding="utf-8")
ENHANCEMENTS = (ROOT / "enhancements.css").read_text(encoding="utf-8")
SCRIPT = (ROOT / "script.js").read_text(encoding="utf-8")


class SpagnuoloSiteTests(unittest.TestCase):
    def test_real_photography_replaces_all_placeholders(self):
        expected = [
            "assets/alessandra-spagnuolo.webp",
            "assets/environment/ambiente-cores.webp",
            "assets/environment/ambiente-colecao.webp",
            "assets/client-media/pes-escalda.webp",
            "assets/gallery/estudio-01.webp",
            "assets/client-media/pes-candle.webp",
            "assets/gallery/hero-unhas-brancas-peroladas.webp",
            "assets/gallery/hero-unhas-vermelhas-close.webp",
            "assets/gallery/portfolio-mao-tatuada-azul.webp",
            "assets/gallery/portfolio-nude-linhas-brancas.webp",
            "assets/gallery/portfolio-prateado-video.webp",
            "assets/gallery/portfolio-cromado-rosa-video.webp",
            "assets/gallery/portfolio-preto-laco-video.webp",
            "assets/gallery/portfolio-nude-clean.webp",
        ]
        for relative in expected:
            self.assertIn(relative, HTML)
            self.assertTrue((ROOT / relative).is_file(), relative)
        self.assertNotRegex(HTML.lower(), r"placeholder|a selecionar|será inserida")

    def test_reconstruction_card_uses_the_sharp_white_photo(self):
        title_position = HTML.index("Reconstrução & fortalecimento")
        card_prefix = HTML[title_position - 500:title_position]
        self.assertIn("hero-unhas-brancas-peroladas.webp", card_prefix)
        self.assertNotIn("unhas-naturais.webp", card_prefix)

    def test_featured_studio_hero_keeps_the_complete_nails_visible(self):
        self.assertIn(".hero-shot:nth-child(2) img{object-fit:contain", CSS)

    def test_premium_environment_and_spa_photos_replace_the_rejected_photo(self):
        expected = [
            "assets/environment/ambiente-cores.webp",
            "assets/environment/ambiente-colecao.webp",
            "assets/client-media/pes-escalda.webp",
            "assets/client-media/pes-candle.webp",
            "assets/client-media/pes-resultado.webp",
        ]
        for relative_path in expected:
            self.assertIn(relative_path, HTML)
            self.assertTrue((ROOT / relative_path).is_file())
        self.assertNotIn("assets/atendimento-spagnuolo.webp", HTML)

    def test_whatsapp_is_live_and_uses_confirmed_public_number(self):
        self.assertGreaterEqual(HTML.count("wa.me/5547996837007"), 3)
        self.assertNotIn("data-whatsapp", HTML)
        self.assertNotIn("data-dialog", HTML)
        self.assertIn("Quero agendar um atendimento", HTML)

    def test_booksy_proof_is_specific_and_sourced(self):
        self.assertRegex(HTML, r"5[,.]0")
        self.assertIn("323 avaliações", HTML)
        self.assertIn("Simplesmente impecável, excelente trabalho", HTML)
        self.assertIn("Franciele Reinert", HTML)
        self.assertIn("Cliente confirmada no Booksy", HTML)

    def test_booksy_rating_does_not_cover_the_hero_photos(self):
        copy_block = re.search(r'<div class="hero-copy-block">(.*?)</div>\s*<div class="hero-visual', HTML, re.S)
        visual_block = re.search(r'<div class="hero-visual.*?</div>\s*<a class="scroll-cue"', HTML, re.S)
        self.assertIsNotNone(copy_block)
        self.assertIsNotNone(visual_block)
        self.assertIn('class="hero-rating"', copy_block.group(1))
        self.assertNotIn('class="hero-rating"', visual_block.group(0))
        self.assertIn("position:static", CSS)

    def test_review_cards_use_clear_portfolio_photos_without_implying_ownership(self):
        reviews = re.search(r'<section class="reviews.*?</section>', HTML, re.S)
        self.assertIsNotNone(reviews)
        self.assertIn('src="assets/gallery/portfolio-prateado-video.webp"', reviews.group(0))
        self.assertIn('src="assets/gallery/portfolio-cromado-rosa-video.webp"', reviews.group(0))
        self.assertIn('src="assets/gallery/hero-unhas-vermelhas-close.webp"', reviews.group(0))
        self.assertGreaterEqual(reviews.group(0).count("Foto do portfólio"), 3)

    def test_all_nail_photos_come_from_yesterdays_batch_except_the_featured_keep(self):
        allowed = {
            "assets/gallery/estudio-01.webp",
            "assets/gallery/hero-unhas-brancas-peroladas.webp",
            "assets/gallery/hero-unhas-vermelhas-close.webp",
            "assets/gallery/portfolio-nude-linhas-brancas.webp",
            "assets/gallery/portfolio-mao-tatuada-azul.webp",
            "assets/gallery/portfolio-prateado-video.webp",
            "assets/gallery/portfolio-cromado-rosa-video.webp",
            "assets/gallery/portfolio-preto-laco-video.webp",
            "assets/gallery/portfolio-nude-clean.webp",
        }
        referenced = {
            item.split("?", 1)[0]
            for item in re.findall(r'assets/gallery/[^"\s]+', HTML)
        }
        self.assertEqual(referenced, allowed)

    def test_primary_conversion_routes_are_present(self):
        self.assertGreaterEqual(HTML.count("booksy.com/pt-br/111694_spagnuolo-designer"), 5)
        self.assertGreaterEqual(HTML.count("instagram.com/spagnuolodesigner"), 2)
        self.assertIn("Agendar pelo Booksy", HTML)
        self.assertIn("Falar pelo WhatsApp", HTML)

    def test_client_signature_phrase_leads_the_hero(self):
        hero = re.search(r'<h1 id="hero-title">(.*?)</h1>', HTML, re.S)
        self.assertIsNotNone(hero)
        hero_text = re.sub(r"<[^>]+>", " ", hero.group(1))
        hero_text = re.sub(r"\s+", " ", hero_text).strip()
        self.assertEqual(
            hero_text,
            "Mais do que unhas perfeitas, uma experiência de cuidado que revela a sua melhor versão.",
        )

    def test_accessible_images_and_reduced_motion(self):
        images = re.findall(r"<img\b[^>]*>", HTML)
        self.assertGreaterEqual(len(images), 7)
        for image in images:
            self.assertRegex(image, r'alt="[^"]*"')
            self.assertRegex(image, r"width=|class=")
        self.assertIn("prefers-reduced-motion", CSS)

    def test_no_unverified_or_draft_language(self):
        forbidden = ["aproximadamente 35", "aproximadamente 9", "canal em preparação", "prévia local para aprovação visual"]
        for text in forbidden:
            self.assertNotIn(text, HTML.lower())

    def test_color_variety_is_visible_and_specific(self):
        self.assertIn("Mais de 1.000 opções de esmaltes", HTML)
        self.assertIn("<strong>+1.000</strong><span>opções de<br>esmaltes</span>", HTML)
        self.assertIn('class="studio-color-note"', HTML)
        self.assertIn('class="about-accent about-photo"', HTML)
        self.assertNotIn('assets/alessandra-retrato-vermelho.webp', HTML)
        self.assertGreaterEqual(HTML.count('src="assets/alessandra-spagnuolo.webp"'), 2)
        hero = re.search(r'<section class="hero".*?</section>', HTML, re.S)
        self.assertIn("portfolio-cromado-rosa-video.webp", hero.group(0))
        self.assertIn("hero-unhas-vermelhas-close.webp", hero.group(0))
        self.assertNotIn("hero-unhas-brancas-peroladas.webp", hero.group(0))

    def test_location_uses_a_responsive_google_map(self):
        self.assertIn('class="google-map"', HTML)
        self.assertIn('https://www.google.com/maps?', HTML)
        self.assertIn('output=embed', HTML)
        self.assertIn('loading="lazy"', HTML)
        self.assertRegex(CSS, r"\.google-map\{[^}]*min-height:")
        self.assertRegex(CSS, r"@media\(max-width:640px\).*?\.google-map\{[^}]*min-height:")

    def test_header_uses_the_official_booksy_logo_instead_of_an_invented_monogram(self):
        self.assertIn("assets/logo-spagnuolo-oficial-wordmark.webp", HTML)
        self.assertNotIn("assets/logo-spagnuolo-oficial.webp", HTML)
        self.assertNotIn('class="brand-mark"', HTML)
        self.assertTrue((ROOT / "assets/logo-spagnuolo-oficial-wordmark.webp").is_file())

    def test_portfolio_opens_a_responsive_high_resolution_gallery(self):
        self.assertIn('data-gallery-open', HTML)
        self.assertIn('class="gallery-dialog"', HTML)
        self.assertIn('data-gallery-prev', HTML)
        self.assertIn('data-gallery-next', HTML)
        self.assertIn('data-gallery-close', HTML)
        dialog = re.search(r'<dialog class="gallery-dialog".*?</dialog>', HTML, re.S)
        self.assertIsNotNone(dialog)
        expected = [
            "assets/gallery/estudio-01.webp",
            "assets/gallery/hero-unhas-vermelhas-close.webp",
            "assets/gallery/portfolio-cromado-rosa-video.webp",
            "assets/gallery/portfolio-preto-laco-video.webp",
            "assets/gallery/portfolio-prateado-video.webp",
            "assets/gallery/portfolio-mao-tatuada-azul.webp",
            "assets/gallery/hero-unhas-brancas-peroladas.webp",
            "assets/gallery/portfolio-nude-linhas-brancas.webp",
            "assets/gallery/portfolio-nude-clean.webp",
        ]
        gallery_sources = re.findall(r'data-gallery-src="([^"]+)"', dialog.group(0))
        self.assertEqual(gallery_sources, expected)
        self.assertEqual(len(gallery_sources), 9)
        for relative in expected:
            self.assertTrue((ROOT / relative).is_file(), relative)
        for old_number in range(2, 11):
            self.assertNotIn(f"assets/gallery/estudio-{old_number:02d}.webp", dialog.group(0))
        self.assertIn('data-gallery-open="0"', HTML)
        self.assertIn('data-gallery-open="3"', HTML)
        self.assertIn('data-gallery-open="6"', HTML)
        self.assertIn("touchstart", SCRIPT)
        self.assertIn("ArrowRight", SCRIPT)
        self.assertIn("ArrowLeft", SCRIPT)
        self.assertRegex(CSS, r"\.gallery-dialog")

    def test_gallery_preserves_the_two_client_approved_images(self):
        dialog = re.search(r'<dialog class="gallery-dialog".*?</dialog>', HTML, re.S)
        self.assertIsNotNone(dialog)
        self.assertIn("assets/gallery/portfolio-mao-tatuada-azul.webp", dialog.group(0))
        self.assertIn("assets/gallery/portfolio-nude-linhas-brancas.webp", dialog.group(0))

    def test_cinematic_motion_is_progressive_and_interactive(self):
        self.assertIn("data-scroll-progress", HTML)
        self.assertIn("data-hero-reel", HTML)
        self.assertEqual(HTML.count("data-hero-shot"), 4)
        self.assertEqual(HTML.count("data-hero-go"), 4)
        hero_block = re.search(r'<div class="hero-photo-wrap".*?</div>\s*<div class="hero-reel-nav"', HTML, re.S)
        self.assertIsNotNone(hero_block)
        hero_sources = re.findall(r'<img src="([^"]+)"', hero_block.group(0))
        self.assertEqual(
            hero_sources,
            [
                "assets/alessandra-spagnuolo.webp",
                "assets/gallery/estudio-01.webp",
                "assets/gallery/portfolio-cromado-rosa-video.webp",
                "assets/gallery/hero-unhas-vermelhas-close.webp",
            ],
        )
        self.assertIn("Nude rosado com glitter", SCRIPT)
        self.assertIn("Cromado rosa e dourado", SCRIPT)
        self.assertIn("Vermelho clássico", SCRIPT)
        self.assertIn("position:static", CSS)
        self.assertIn("IntersectionObserver", SCRIPT)
        self.assertIn("requestAnimationFrame", SCRIPT)
        self.assertIn("prefers-reduced-motion", SCRIPT)
        self.assertIn("motion-ready", SCRIPT)
        self.assertRegex(CSS, r"\.motion-ready\s+\.reveal")
        self.assertRegex(CSS, r"\.scroll-progress")

    def test_client_experience_carousel_uses_real_proof(self):
        self.assertIn("featured-testimonial", HTML)
        self.assertIn("Veja a experiência em vídeo", HTML)
        self.assertIn('poster="assets/client-media/depoimento-cliente-poster-sorriso.webp"', HTML)
        self.assertIn("data-testimonial-track", HTML)
        self.assertIn("data-testimonial-prev", HTML)
        self.assertIn("data-testimonial-next", HTML)
        self.assertGreaterEqual(HTML.count('class="testimonial-slide'), 3)
        self.assertIn("assets/client-media/depoimento-cliente-web.mp4", HTML)
        self.assertTrue((ROOT / "assets/client-media/depoimento-cliente-web.mp4").is_file())
        self.assertIn("object-fit: contain", ENHANCEMENTS)
        self.assertIn("height: 680px", ENHANCEMENTS)
        self.assertIn("scrollLeft", SCRIPT)

    def test_comfort_and_specialized_care_are_visible(self):
        self.assertIn("Cuidado dos pés com conforto", HTML)
        self.assertIn("Atendimento em maca", HTML)
        self.assertIn("massagem", HTML)
        self.assertIn("spa", HTML)
        self.assertIn("não substitui avaliação médica", HTML)
        self.assertNotIn('class="comfort-highlights', HTML)
        self.assertEqual(HTML.count('class="feet-step reveal"'), 3)
        self.assertNotIn("assets/atendimento-spagnuolo.webp", HTML)

    def test_feet_experience_section_shows_comfort_without_autoplay(self):
        section = re.search(r'<section class="feet-experience.*?</section>', HTML, re.S)
        self.assertIsNotNone(section)
        content = section.group(0)
        self.assertIn('id="experiencia-pes"', content)
        self.assertIn("Cuidado dos pés com conforto", content)
        self.assertIn("confortavelmente deitada", content)
        self.assertIn("assets/client-media/pes-atendimento-maca.mp4", content)
        self.assertIn("assets/client-media/pes-atendimento-poster.webp", content)
        self.assertIn("assets/client-media/pes-escalda.webp", content)
        self.assertIn("assets/client-media/pes-candle.webp", content)
        self.assertIn("assets/client-media/pes-resultado.webp", content)
        self.assertIn("controls", content)
        self.assertNotIn("autoplay", content)
        self.assertRegex(CSS, r"\.feet-experience")
        self.assertIn("feet-step-copy", content)
        self.assertIn("height:170px", CSS)
        self.assertIn("grid-template-columns:42% 58%", CSS)
        self.assertIn('class="feet-video-media"', content)
        self.assertIn(".feet-video-media{object-fit:contain", CSS)

    def test_optional_licensed_background_music_requires_user_action(self):
        audio = re.search(r'<audio id="ambient-audio".*?</audio>', HTML, re.S)
        self.assertIsNotNone(audio)
        self.assertIn("assets/audio/bossa-antigua-kevin-macleod.mp3", audio.group(0))
        self.assertIn("assets/audio/bossa-antigua-kevin-macleod.ogg", audio.group(0))
        self.assertIn("loop", audio.group(0))
        self.assertNotIn("autoplay", audio.group(0))
        self.assertIn("data-audio-toggle", HTML)
        self.assertIn("Ativar ambiente", HTML)
        self.assertIn("Bossa Antigua", HTML)
        self.assertIn("Kevin MacLeod", HTML)
        self.assertIn("creativecommons.org/licenses/by/4.0", HTML)
        self.assertIn("ambientAudio.play()", SCRIPT)
        self.assertIn("ambientAudio.pause()", SCRIPT)
        self.assertIn("is-playing", SCRIPT)
        self.assertTrue((ROOT / "assets/audio/bossa-antigua-kevin-macleod.mp3").is_file())
        self.assertTrue((ROOT / "assets/audio/bossa-antigua-kevin-macleod.ogg").is_file())
        self.assertTrue((ROOT / "assets/audio/PROVENANCE.md").is_file())


if __name__ == "__main__":
    unittest.main()
