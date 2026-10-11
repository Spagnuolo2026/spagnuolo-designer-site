# Spagnuolo Designer — site institucional

Landing page estática, responsiva e preparada para publicação após aprovação visual final.

## Situação atual

- Código final consolidado localmente.
- Feedback visual e de conteúdo recebido até 7 de outubro de 2026 aplicado.
- 23 testes automatizados aprovados.
- JavaScript validado sem erros de sintaxe.
- Pacote público reduzido aos arquivos realmente usados pela página.
- Nenhum domínio ou ambiente de produção foi ativado por este projeto.

## Estrutura principal

- `index.html` — conteúdo e estrutura da landing page.
- `styles.css`, `stories.css` e `enhancements.css` — identidade visual, responsividade e interações.
- `script.js` — menu, galerias, carrosséis, movimento e áudio opcional.
- `assets/` — fotografias, vídeos e música utilizados na versão final.
- `tests/test_site.py` — testes de contrato do front-end.
- `VALIDACAO.md` — resultado da validação e pendências para publicação.

## Abrir localmente

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

Acesse `http://127.0.0.1:4173`.

## Testes

```bash
python3 -m unittest discover -s tests -v
node --check script.js
```

## Conversão

- Booksy como CTA principal de agendamento.
- WhatsApp Business como canal de conversa.
- Instagram como extensão do portfólio.
- Google Maps para localização e rota.

## Hospedagem prevista

Cloudflare Pages, sem mensalidade de hospedagem. O domínio continua sujeito à renovação anual no Registro.br. A publicação e a conexão do domínio dependem da aprovação visual final e do acesso autenticado pela titular da conta.

## Segurança

O repositório não deve conter senhas, códigos temporários, chaves de acesso, capturas de autenticação ou exportações completas das conversas com a cliente.
