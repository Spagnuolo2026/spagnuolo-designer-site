# Validação — Spagnuolo Designer

**Data:** 9 de outubro de 2026  
**Escopo:** landing page estática e responsiva  
**Status:** código pronto para prévia final; ainda não publicado

## Aprovado pela cliente

- Direção visual premium em azul-marinho, dourado e marfim.
- Manutenção das seções e descrições aprovadas.
- Retirada das fotografias rejeitadas.
- Uso da fotografia correta de Alessandra Spagnuolo.
- Maior variedade de cores e trabalhos no portfólio.
- Destaque para o atendimento dos pés com conforto, spa e atendimento em maca.
- Vídeos sem reprodução automática.
- Ambiente acolhedor e música apenas como recurso opcional.
- Hospedagem sem mensalidade, com titularidade e acesso da empresa.

## Aplicado no código

- Hero editorial com Alessandra e trabalhos selecionados.
- Galeria navegável com nove trabalhos e variedade de cores.
- Seção “Cuidado dos pés com conforto”, com vídeo e três etapas visuais.
- Vídeo de depoimento com poster e reprodução sob ação da visitante.
- Música licenciada “Bossa Antigua”, de Kevin MacLeod, sem autoplay e com controle persistente.
- Fotografias reais do estúdio, dos atendimentos e do portfólio.
- Prova social do Booksy com nota 5,0 e 323 avaliações na referência validada.
- CTA principal para Booksy, WhatsApp, Instagram e Google Maps.
- Menu móvel, CTA fixo, FAQ, galeria, carrosséis e respeito a `prefers-reduced-motion`.
- 22 arquivos públicos de mídia referenciados, todos presentes.

## Verificações executadas

- `python3 -m unittest discover -s tests -v`: **23/23 aprovados**.
- `node --check script.js`: aprovado.
- Referências a mídia: **22/22 existentes**.
- Senhas, tokens, chaves e códigos temporários: não devem integrar o pacote público.
- Pacote de mídia utilizado pela página: aproximadamente 22,1 MB.

## Pendências antes de publicar

1. Abrir a prévia definitiva no computador e no celular para aprovação de Sulana.
2. Confirmar novamente o número do WhatsApp e a quantidade de avaliações do Booksy.
3. Criar o repositório definitivo sob a titularidade combinada com a cliente.
4. Criar o projeto gratuito no Cloudflare Pages.
5. A titular deve entrar no Registro.br e autorizar a alteração de DNS; senhas e códigos não serão digitados pela automação.
6. Revisar e, se necessário, rotacionar as credenciais de acesso antes da conexão do domínio.
7. Conectar o domínio somente após o OK explícito de publicação.
8. Verificar HTTPS, domínio canônico, vídeos, áudio, Booksy, WhatsApp, Instagram e Maps já no endereço público.

## Estado externo verificado

- Não há servidor de prévia ativo neste momento.
- `spagnuolodesigner.com.br` ainda não resolve no DNS.
- Nenhuma publicação de produção foi realizada.
