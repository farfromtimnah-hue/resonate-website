#!/usr/bin/env python3
"""Builds resonate-website/public/fluxo/sistema/index.html (PT default, EN toggle).
Images and the PDF are served by the Apex worker from R2 (/api/pitch/<name>),
never committed to the public website repo (they carry JM's header photos)."""
import html, os

OUT = os.path.expanduser("~/resonate-website/public/fluxo/sistema/index.html")
A = "https://apex-api.farfromtimnah.workers.dev/api/pitch/"
DOC = {
    "estimate": "https://doc.resonateai.online/marlow-pool-and-patio/est-0023-daniel-and-marisa-whitfield-2mw44neq",
    "contract": "https://doc.resonateai.online/marlow-pool-and-patio/con-0016-wub98rs9",
    "invoice": "https://doc.resonateai.online/marlow-pool-and-patio/inv-0022-daniel-and-marisa-whitfield-gqkeqswm",
    "receipt": "https://apex.resonateai.online/receipt-view?t=6d25692423cef68a1c2e3df52e6f5672657ac5d70314e6b1",
    "card": "https://apex.resonateai.online/card?t=02e180941ff22eda23b9b8d385826c65652a7f40bc59ef7c",
    "referral": "https://apex.resonateai.online/referral.html?p=xvvmrs2xah3yke&lang=en",
}

def t(pt, en, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-pt="{html.escape(pt, quote=True)}" data-en="{html.escape(en, quote=True)}">{pt}</{tag}>'

def ul(items):
    return "<ul>" + "".join(f"<li>{t(pt, en)}</li>" for pt, en in items) + "</ul>"

ESTIMATE = [
    ("Monta a partir do lead: nome, telefone e endereço já vêm preenchidos.", "Built from the lead: name, phone and address come filled in."),
    ("Opções Best, Better e Good, com botão para duplicar a opção nas outras.", "Best, Better and Good options, with one button to copy an option into the others."),
    ("Produtos da tabela de preços, com cálculo por linha e subtotal por categoria.", "Products from the price list, with per-line math and a subtotal per category."),
    ("Custo e margem internos, com aviso de margem baixa. O cliente nunca vê.", "Internal cost and margin, with a low-margin warning. The customer never sees it."),
    ("Sinal e parcelas por etapa, e o aviso da Flórida quando o sinal passa de 10%.", "Deposit and staged payments, and the Florida notice when the deposit is over 10%."),
    ("Validade, o que está incluso e o que não está, em texto claro.", "Valid-until date, what is included and what is not, in plain words."),
    ("O cliente escolhe a opção e assina no celular, sem criar conta.", "The customer picks an option and signs on the phone, with no account."),
    ("Aceitou: o lead fecha e o projeto é criado sozinho.", "Once accepted, the lead closes and the project is created on its own."),
]
CONTRACT = [
    ("Nasce do orçamento aceito: preço, escopo e parcelas já estão lá.", "Built from the accepted estimate: price, scope and payments are already there."),
    ("Avisos da Flórida por regra: gravame (713.015), Recovery Fund, cancelamento em 3 dias e documentos de piscina (515).", "Florida notices by rule: lien (713.015), Recovery Fund, 3-day cancellation and pool documents (515)."),
    ("A empresa assina primeiro; o cliente assina depois, digitando ou desenhando.", "The company signs first; the customer signs after, typed or drawn."),
    ("Cada assinatura grava nome, data, hora, aparelho e um código de verificação (SHA-256).", "Every signature records name, date, time, device and a verification code (SHA-256)."),
    ("PDF feito no servidor e guardado no momento da assinatura: nunca muda.", "PDF made on the server and stored at signing: it never changes."),
    ("Aditivos com total antigo, mudança e total novo; o cliente assina cada um.", "Change orders show old total, change and new total; the customer signs each one."),
    ("Preço do contrato editável, com a linha de ajuste negociado à vista do cliente.", "Editable contract price, with the negotiated adjustment line shown to the customer."),
    ("Vendedor pode assinar pela empresa quando o dono autoriza.", "A salesperson can sign for the company when the owner authorizes it."),
]
INVOICE = [
    ("Uma fatura por etapa, criada do contrato com um toque.", "One invoice per payment step, created from the contract in one tap."),
    ("Mostra total do contrato, pago até hoje, esta fatura e o saldo restante.", "Shows contract total, paid to date, this invoice and the remaining balance."),
    ("Registrar pagamento: valor total ou parcial, só nas formas que a empresa aceita.", "Record a payment: full or partial, only in the methods the business accepts."),
    ("Recibo automático para cada pagamento, com o saldo congelado na data.", "An automatic receipt for every payment, with the balance frozen on that date."),
    ("Crédito, reembolso e juros por atraso, sempre com motivo registrado.", "Credits, refunds and late fees, always with a recorded reason."),
    ("Pagamentos entram sozinhos no Financeiro, sem digitar de novo.", "Payments post to Finance on their own, with no re-typing."),
    ("Aditivo assinado atualiza as faturas e avisa quando uma já enviada mudou.", "A signed change order updates the invoices and flags one that was already sent."),
    ("O vendedor informa um pagamento; o dono confirma antes de valer.", "A salesperson reports a payment; the owner confirms it before it counts."),
]
ACROSS = [
    ("Enviado do celular do vendedor, por WhatsApp ou mensagem, nunca de um e-mail genérico.", "Sent from the salesperson's own phone, by WhatsApp or text, never from a generic email."),
    ("O link chega com o logo e o nome da empresa, e o endereço tem o nome do cliente.", "The link arrives with the business's logo and name, and the address carries the customer's name."),
    ("Capa premium: mais de 50 fotos por ramo, ou a foto da própria empresa, com o logo e as cores dela.", "Premium header: more than 50 curated photos by trade, or the business's own photo, with its logo and colors."),
    ("O documento enviado guarda o visual do dia do envio, mesmo se a empresa mudar o logo depois.", "A sent document keeps the look it was sent with, even if the business changes its logo later."),
    ("Mensagens de envio editáveis, com histórico de cada mudança.", "Editable send messages, with a history of every change."),
    ("Cartão de contato do vendedor, que o cliente salva no celular, com o link de indicação dele.", "The salesperson's contact card, which the customer saves to the phone, with their own referral link."),
    ("Indicação chega direto para o vendedor certo.", "A referral goes straight to the right salesperson."),
    ("O dono trabalha em português; o cliente americano recebe tudo em inglês.", "The owner works in Portuguese; the American customer receives everything in English."),
    ("Nada é digitado duas vezes: lead, orçamento, contrato, projeto e fatura estão ligados.", "Nothing is typed twice: lead, estimate, contract, project and invoice are connected."),
]

COMPLAINTS = [
    ("Mais de 60% dos orçamentos nunca foram abertos; o e-mail genérico da ferramenta cai no spam.",
     "Over 60% of estimates were never opened; the software's generic email lands in spam.",
     "Avaliação pública, Trustpilot, dez/2025", "Public review, Trustpilot, Dec 2025", "",
     "Sai do celular do vendedor, por WhatsApp ou mensagem, com o logo da empresa no link.",
     "It goes from the salesperson's own phone, by WhatsApp or text, with the business's logo on the link."),
    ("O link de contrato parece golpe; quem recebe liga para confirmar quem mandou.",
     "The contract link looks like a scam; recipients call to confirm who sent it.",
     "Avaliações públicas, Trustpilot, ago e set/2026", "Public reviews, Trustpilot, Aug and Sep 2026", "",
     "Chega de alguém que o cliente conhece, com o nome e o logo da empresa e o nome dele no endereço.",
     "It arrives from someone the customer knows, with the business's name and logo and their own name in the address."),
    ("O cliente não reconhece o remetente, e o documento fica sem abrir ou vai para o spam.",
     "The customer does not recognize the sender, so the document sits unopened or goes to spam.",
     "Avaliações públicas, Trustpilot, set/2026 e Capterra, jan/2025", "Public reviews, Trustpilot, Sep 2026 and Capterra, Jan 2025", "",
     "O cliente reconhece quem manda: é o vendedor que ele conheceu, com o logo da empresa.",
     "The customer knows who sent it: the salesperson they met, with the company's logo."),
    ("Suporte só por chatbot, ou semanas para ter resposta.",
     "Support by chatbot only, or weeks to get an answer.",
     "Avaliações públicas, Trustpilot, jun/2026", "Public reviews, Trustpilot, Jun 2026", "",
     "Um consultor acompanha a empresa por dentro do sistema.",
     "A consultant works alongside the business, inside the system."),
    ("Aditivo não reduz escopo e não há histórico de versões.",
     "A change order cannot reduce scope, and there is no version history.",
     "Avaliações públicas, Capterra, 2022 e 2024", "Public reviews, Capterra, 2022 and 2024", "",
     "Aditivo tira ou põe itens, com crédito pelo preço cobrado. Cada revisão fica guardada.",
     "A change order adds or removes items, crediting at the price charged. Every revision is kept."),
    ("Fatura final que não bate com o orçamento assinado.",
     "A final invoice that does not match the signed estimate.",
     "Fórum público de donos de casa", "Public homeowner forum", "",
     "Cada fatura mostra o contrato, os aditivos, o que já foi pago e o saldo.",
     "Every invoice shows the contract, the change orders, what was paid and the balance."),
    ("Dados digitados duas vezes entre módulos que não conversam.",
     "Data typed twice between modules that do not talk to each other.",
     "Avaliação pública, Capterra, 2021", "Public review, Capterra, 2021", "",
     "Lead, orçamento, contrato, projeto e fatura são o mesmo registro.",
     "Lead, estimate, contract, project and invoice are one record."),
    ("Nenhuma dessas ferramentas funciona em português.",
     "None of these tools works in Portuguese.",
     "Pesquisa Resonate, set/2026", "Resonate research, Sep 2026", "",
     "O sistema inteiro em português e inglês; o documento do cliente sai em inglês.",
     "The whole system in Portuguese and English; the customer's document goes out in English."),
]

LEGAL = [
    ("\"Esse dano já estava aí.\"", "\"That damage was already there.\"", "Prática recomendada: fotografar antes de começar", "Recommended practice: photograph before starting",
     "Fotos de antes da obra, que o cliente reconhece no momento de assinar o contrato. Elas vão anexas ao contrato.", "Before-work photos the customer acknowledges when signing the contract. They are attached to the contract."),
    ("Serviço mal feito, ou recusa em corrigir.", "Poor workmanship, or refusing to fix it.", "Reclamações ao DBPR da Flórida", "Complaints to Florida's DBPR",
     "Vistoria final com lista de pendências assinada pelo cliente, e o processo do capítulo 558 escrito no contrato.", "A final walkthrough with a punch list the customer signs, and the chapter 558 process written into the contract."),
    ("Subcontratado ou fornecedor sem pagamento, e gravame na casa.", "An unpaid sub or supplier, and a lien on the house.", "Reclamações ao DBPR da Flórida", "Complaints to Florida's DBPR",
     "Controle de cada Notice to Owner e liberação de gravame, e a declaração de pagamento final.", "Tracking of every Notice to Owner and lien release, and the final payment affidavit."),
    ("Atraso na obra.", "Job delays.", "Reclamações ao DBPR da Flórida", "Complaints to Florida's DBPR",
     "Condições de início, clima e atrasos escritas no contrato; cada aditivo atualiza o prazo.", "Start conditions, weather and delays written into the contract; every change order updates the deadline."),
    ("Obra abandonada.", "An abandoned job.", "Reclamações ao DBPR da Flórida", "Complaints to Florida's DBPR",
     "Pagamentos ligados a etapas da obra, com regras de suspensão e rescisão no contrato.", "Payments tied to job stages, with suspension and termination terms in the contract."),
    ("O cliente muda o preço depois de assinado.", "The customer rewrites the price after signing.", "Empreiteiros relatam no X", "Contractors report it on X",
     "Toda mudança é um aditivo assinado. A cópia assinada tem um código de verificação e nunca muda.", "Every change is a signed change order. The signed copy carries a verification code and never changes."),
    ("Briga sobre o cancelamento em 3 dias.", "A dispute over the 3-day cancellation.", "Lei da Flórida, venda em casa (501.031)", "Florida law, home solicitation sale (501.031)",
     "Aviso de cancelamento com a data real do prazo, calculada no momento da assinatura.", "A cancellation notice with the real deadline date, calculated at signing."),
    ("Subcontratado sem licença.", "An unlicensed subcontractor.", "Reclamações no condado de Pinellas", "Complaints in Pinellas County",
     "Licença e seguro de cada subcontratado guardados, com aviso antes de vencer.", "Each subcontractor's license and insurance on file, with an alert before it expires."),
    ("Sinal alto e a obra não começa.", "A large deposit and the job never starts.", "Lei da Flórida (489.126)", "Florida law (489.126)",
     "Aviso automático quando o sinal passa de 10%: licenças em 30 dias e início em 90.", "An automatic notice when the deposit is over 10%: permits within 30 days, start within 90."),
    ("Obra feita sem contrato.", "Work done with no contract.", "Prática recomendada: nunca começar só com orçamento", "Recommended practice: never start on an estimate alone",
     "Aviso em toda obra acima de $2,500 sem contrato; depois de 7 dias, o consultor também vê.", "A warning on every job over $2,500 with no contract; after 7 days the consultant sees it too."),
]

TRUST = [
    ("O cliente final não compra do software.", "The homeowner does not buy from the software.",
     "Em qualquer uma dessas ferramentas, o dono da casa vê o orçamento da sua empresa. Ele não escolhe o Jobber; escolhe você.",
     "In any of these tools, the homeowner sees your company's estimate. They do not choose Jobber; they choose you."),
    ("Onde a marca deles aparece, atrapalha.", "Where their brand shows, it gets in the way.",
     "E-mail genérico (jobbermail.com) cai no spam, e link de assinatura parece golpe. Está nas avaliações públicas acima.",
     "A generic email (jobbermail.com) lands in spam, and a signing link looks like a scam. It is in the public reviews above."),
    ("No Apex, tudo leva a sua marca.", "In Apex, everything carries your brand.",
     "Sai do celular do seu vendedor, com o seu logo, o seu nome e o nome do cliente no endereço do link.",
     "It goes from your salesperson's own phone, with your logo, your name and the customer's name in the link address."),
]

Y, N = '<span class="yes">✓</span>', '<span class="no">✕</span>'
def P(pt, en): return f'<span class="part">{t(pt, en)}</span>'
ROWS = [
    ("cat", "Documentos", "Documents"),
    ("Orçamentos", "Estimates", Y, Y, P("+$150/mês (Business)", "+$150/mo (Business)"), Y),
    ("Opções Best, Better e Good", "Best, Better and Good options", N, N, P("+$150/mês (Business)", "+$150/mo (Business)"), Y),
    ("Contrato a partir de um modelo, assinado pelas duas partes", "Contract from a template, signed by both parties", N, Y, Y, Y),
    ("Contrato montado sozinho a partir do orçamento aceito, com os avisos da Flórida", "Contract built automatically from the accepted estimate, with the Florida notices", N, N, N, Y),
    ("Assinatura eletrônica", "Electronic signature", Y, Y, Y, Y),
    ("Avisos da Flórida aplicados por regra", "Florida notices applied by rule", N, N, N, Y),
    ("Aditivos (change orders)", "Change orders", N, Y, N, Y),
    ("Faturas por etapa, com sinal", "Staged invoices, with deposit", Y, Y, P("+$150/mês (Business)", "+$150/mo (Business)"), Y),
    ("Link com logo da empresa no WhatsApp e iMessage", "Link with the business logo in WhatsApp and iMessage", N, N, N, Y),
    ("Visual do documento congelado no envio", "Document look frozen at send", N, N, N, Y),
    ("Cartão de contato do vendedor com link de indicação", "Salesperson contact card with a referral link", N, N, N, Y),
    ("cat", "Operação", "Operations"),
    ("Agendamento e calendário", "Scheduling and calendar", Y, P("+$38/mês (plano Run)", "+$38/mo (Run plan)"), N, Y),
    ("Link de marcação para o cliente", "Booking link for the customer", Y, N, N, Y),
    ("Pipeline de leads / CRM", "Lead pipeline / CRM", N, N, N, Y),
    ("Projetos com custo e margem", "Projects with cost and margin", N, N, N, Y),
    ("Portal do cliente", "Client portal", Y, N, N, Y),
    ("Logins por vendedor, cada um vê só os seus", "Logins per salesperson, each sees only their own", P("5 usuários", "5 users"), N, P("5 usuários", "5 users"), Y),
    ("cat", "Proteção na Flórida", "Protection in Florida"),
    ("Aviso de gravame (713.015), Recovery Fund e cancelamento em 3 dias, por regra", "Lien notice (713.015), Recovery Fund and 3-day cancellation, by rule", N, N, N, Y),
    ("Documentos de piscina (capítulo 515) e recurso de segurança no contrato", "Pool documents (chapter 515) and safety feature in the contract", N, N, N, Y),
    ("Aviso automático quando o sinal passa de 10%", "Automatic notice when the deposit is over 10%", N, N, N, Y),
    ("Juros por atraso dentro do limite da Flórida (18% ao ano)", "Late fees within the Florida cap (18% a year)", N, N, N, Y),
    ("cat", "Contra disputas", "Dispute prevention"),
    ("Fotos de antes da obra, reconhecidas pelo cliente ao assinar", "Before-work photos, acknowledged by the customer at signing", N, N, N, Y),
    ("Vistoria final e lista de pendências assinadas", "Final walkthrough and punch list, signed", N, N, N, Y),
    ("Controle de Notice to Owner e liberação de gravame", "Notice to Owner and lien release tracking", N, N, N, Y),
    ("Declaração de pagamento final (affidavit), com ajuda para o cartório", "Final payment affidavit, with notary help", N, N, N, Y),
    ("Licença e seguro dos subcontratados, com aviso de vencimento", "Subcontractor license and insurance, with expiry alerts", N, N, N, Y),
    ("Aviso de obra acima de $2,500 sem contrato", "Warning on any job over $2,500 with no contract", N, N, N, Y),
    ("Cópia assinada com código de verificação, que nunca muda", "Signed copy with a verification code, never altered", N, N, Y, Y),
    ("cat", "Venda", "Sales"),
    ("Três preços por negócio: orçamento, contrato e final", "Three prices on every deal: estimate, contract and final", N, N, N, Y),
    ("Cartão de contato do vendedor, salvo no celular do cliente", "Salesperson contact card, saved to the customer's phone", N, N, N, Y),
    ("Indicação do cliente creditada ao vendedor certo", "Customer referrals credited to the right salesperson", N, N, N, Y),
    ("Vendedor assina pela empresa quando o dono autoriza", "Salesperson signs for the company when the owner authorizes", N, N, N, Y),
    ("cat", "Controle do dinheiro", "Money control"),
    ("Pagamento informado pelo vendedor, confirmado pelo dono", "Payment reported by the salesperson, confirmed by the owner", N, N, N, Y),
    ("Recibo automático a cada pagamento", "Automatic receipt for every payment", N, N, N, Y),
    ("Aditivo que tira itens credita pelo preço cobrado", "A change order that removes items credits the price charged", N, N, N, Y),
    ("Histórico de cada mudança de valor do projeto", "History of every change to the project value", N, N, N, Y),
    ("cat", "Apresentação", "Presentation"),
    ("Capa premium com mais de 50 fotos por ramo, logo e cores da empresa", "Premium header with more than 50 photos by trade, the business's logo and colors", N, N, N, Y),
    ("O dono trabalha em português; o cliente recebe em inglês", "The owner works in Portuguese; the customer receives English", N, N, P("português de Portugal", "European Portuguese"), Y),
    ("cat", "Gestão e consultoria", "Management and consulting"),
    ("Diagnóstico do negócio (7 instrumentos)", "Business diagnostic (7 instruments)", N, N, N, Y),
    ("Mapa do fluxo do dinheiro", "Money flow map", N, N, N, Y),
    ("Registro diário e metas mensais", "Daily log and monthly goals", N, N, N, Y),
    ("Parceiros de indicação, com atribuição automática", "Referral partners, with automatic attribution", N, N, N, Y),
    ("Base de Ouro (carteira de recompra)", "Gold Base (repeat-customer book)", N, N, N, Y),
    ("Português e inglês, o sistema inteiro", "Portuguese and English, the whole system", N, N, P("português de Portugal", "European Portuguese"), Y),
    ("Consultor acompanha por dentro", "A consultant works alongside, inside the system", N, N, N, Y),
]

def cmp_table():
    h = ['<div class="tbl-wrap cmp"><table><thead><tr>',
         f'<th>{t("Recurso", "Feature")}</th><th class="apexcol">Apex</th><th>Jobber</th><th>Joist</th><th>PandaDoc</th>',
         '</tr></thead><tbody>']
    for r in ROWS:
        if r[0] == "cat":
            h.append(f'<tr class="catrow"><td colspan="5">{t(r[1], r[2])}</td></tr>')
        else:
            h.append(f'<tr><td>{t(r[0], r[1])}</td><td class="apexcol">{r[5]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>')
    h.append('</tbody></table></div>')
    return "".join(h)

def doc_col(key, kpt, ken, hpt, hen, items):
    return f'''<article class="doc">
  <p class="k">{t(kpt, ken)}</p>
  <h3>{t(hpt, hen)}</h3>
  <a class="shot" href="{DOC[key]}" target="_blank" rel="noopener"><img src="{A}{key}.jpg" alt="" loading="lazy"><span class="open">{t("Abrir o documento real ↗", "Open the real document ↗")}</span></a>
  {ul(items)}
</article>'''

def small(key, img, kpt, ken, cpt, cen, link=True):
    inner = f'<img src="{A}{img}.jpg" alt="" loading="lazy">'
    a = f'<a class="shot" href="{DOC[key]}" target="_blank" rel="noopener">{inner}<span class="open">{t("Abrir ↗", "Open ↗")}</span></a>' if link else f'<div class="shot">{inner}</div>'
    return f'<figure class="mini">{a}<figcaption><b>{t(kpt, ken)}</b> {t(cpt, cen)}</figcaption></figure>'

trust_html = "".join('<div class="tr"><h3>' + t(a, b) + '</h3>' + t(c, d, "p") + '</div>' for a, b, c, d in TRUST)

legal_rows = "".join(
    f'<tr><td>{t(a, b)}<span class="src">{t(sp, se)}</span></td><td class="ans">{t(c, d)}</td></tr>'
    for a, b, sp, se, c, d in LEGAL)

complaints_rows = "".join(
    f'<tr><td>{t(a, b)}<span class="src">{(f"<a href={chr(34)}{u}{chr(34)} target={chr(34)}_blank{chr(34)} rel={chr(34)}noopener{chr(34)}>" + t(sp, se) + "</a>") if u else t(sp, se)}</span></td><td class="ans">{t(c, d)}</td></tr>'
    for a, b, sp, se, u, c, d in COMPLAINTS)

PAGE = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Apex · Do lead à fatura</title>
<style>
:root {{
  --navy: #0F1E3D; --navy-2: #1B3255; --gold: #C9A227; --gold-deep: #8A6F2C;
  --flow: #3f7d4e; --page: #FBFAF8; --page-2: #F2F0EB; --card: #FFFFFF;
  --ink: #14171C; --muted: #5A6270; --faint: #8B93A0;
  --line: rgba(20,23,28,0.13); --line-2: rgba(20,23,28,0.07); --shadow: rgba(12,24,41,0.10);
  --sans: Helvetica, Arial, sans-serif; --r: 14px;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{ --page:#0C1829; --page-2:#101F35; --card:#16273F; --ink:#EEF1F5; --muted:#9BA6B6; --faint:#74808F; --line:rgba(238,241,245,0.16); --line-2:rgba(238,241,245,0.09); --shadow:rgba(0,0,0,0.5); --gold-deep:#D8B870; --flow:#63ab75; }}
}}
:root[data-theme="dark"] {{ --page:#0C1829; --page-2:#101F35; --card:#16273F; --ink:#EEF1F5; --muted:#9BA6B6; --faint:#74808F; --line:rgba(238,241,245,0.16); --line-2:rgba(238,241,245,0.09); --shadow:rgba(0,0,0,0.5); --gold-deep:#D8B870; --flow:#63ab75; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--page); color: var(--ink); font-family: var(--sans); font-size: 1.02rem; line-height: 1.55; -webkit-font-smoothing: antialiased; }}
h1, h2, h3 {{ margin: 0; font-weight: 700; line-height: 1.15; letter-spacing: -0.02em; }}
p {{ margin: 0; }}
a {{ color: inherit; }}
.wrap {{ max-width: 74rem; margin: 0 auto; padding: 0 clamp(1rem, 4vw, 2rem); }}
section {{ padding: clamp(3rem, 8vh, 5.5rem) 0; }}
.tint {{ background: var(--page-2); }}
.lang {{ position: fixed; top: .85rem; right: .85rem; z-index: 60; display: flex; gap: 2px; padding: 3px; background: var(--card); border: 1px solid var(--line); border-radius: 999px; box-shadow: 0 1px 3px var(--shadow); }}
.lang button {{ border: 0; background: transparent; cursor: pointer; font: 700 .7rem/1 var(--sans); letter-spacing: .07em; color: var(--muted); padding: .45rem .75rem; border-radius: 999px; }}
.lang button[aria-pressed="true"] {{ background: var(--navy); color: #fff; }}
.hero {{ background: var(--navy); color: #fff; padding: clamp(3.5rem, 10vh, 6rem) 0 clamp(3rem, 8vh, 4.5rem); }}
.hero .logo {{ width: 120px; height: auto; display: block; margin-bottom: 2rem; }}
.hero h1 {{ font-size: clamp(2.1rem, 5.4vw, 3.4rem); max-width: 18ch; }}
.hero .lede {{ margin-top: 1rem; font-size: clamp(1.05rem, 2vw, 1.25rem); color: rgba(255,255,255,0.78); max-width: 46ch; }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: .9rem; margin-top: 2.4rem; }}
.stat {{ border: 1px solid rgba(255,255,255,0.16); border-radius: var(--r); padding: 1rem 1.1rem; background: rgba(255,255,255,0.04); }}
.stat .n {{ font-size: 1.9rem; font-weight: 700; color: var(--gold); letter-spacing: -0.02em; }}
.stat .n small {{ font-size: .9rem; color: rgba(255,255,255,0.6); font-weight: 400; }}
.stat p {{ margin-top: .3rem; font-size: .88rem; color: rgba(255,255,255,0.74); }}
.pdf {{ display: inline-block; margin-top: 2rem; padding: .75rem 1.2rem; border-radius: 999px; border: 1px solid var(--gold); color: var(--gold); text-decoration: none; font-weight: 700; font-size: .9rem; }}
.sec-h h2 {{ font-size: clamp(1.6rem, 3.6vw, 2.3rem); max-width: 24ch; }}
.sec-h p {{ margin-top: .7rem; color: var(--muted); max-width: 60ch; }}
.docs {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2rem; margin-top: 2rem; }}
.doc {{ background: var(--card); border: 1px solid var(--line); border-radius: var(--r); padding: 1.1rem; box-shadow: 0 1px 2px var(--shadow); display: flex; flex-direction: column; }}
.k {{ font: 700 .62rem/1 var(--sans); letter-spacing: .12em; text-transform: uppercase; color: var(--gold-deep); }}
.doc h3 {{ margin-top: .45rem; font-size: 1.12rem; }}
.shot {{ position: relative; display: block; margin-top: .9rem; border-radius: 10px; overflow: hidden; border: 1px solid var(--line); background: #eef0f2; text-decoration: none; }}
.doc .shot {{ height: 430px; }}
.shot img {{ width: 100%; height: 100%; object-fit: cover; object-position: top; display: block; transition: transform .35s ease; }}
a.shot:hover img {{ transform: scale(1.02); }}
.shot .open {{ position: absolute; right: .6rem; bottom: .6rem; background: rgba(15,30,61,0.88); color: #fff; font-size: .74rem; font-weight: 700; padding: .4rem .7rem; border-radius: 999px; }}
.doc ul, .all ul {{ margin: .9rem 0 0; padding-left: 1.1rem; font-size: .88rem; color: var(--muted); }}
.doc li, .all li {{ margin-top: .35rem; }}
.minis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1.4rem; }}
.mini {{ margin: 0; }}
.mini .shot {{ height: 220px; margin-top: 0; }}
.mini figcaption {{ margin-top: .5rem; font-size: .82rem; color: var(--muted); }}
.mini figcaption b {{ color: var(--ink); }}
.all {{ margin-top: 1.4rem; background: var(--card); border: 1px solid var(--line); border-left: 3px solid var(--gold); border-radius: var(--r); padding: 1.1rem 1.3rem; }}
.all ul {{ columns: 2; column-gap: 2rem; }}
.all li {{ break-inside: avoid; }}
.tbl-wrap {{ margin-top: 1.6rem; overflow-x: auto; border: 1px solid var(--line); border-radius: var(--r); background: var(--card); box-shadow: 0 1px 2px var(--shadow); }}
table {{ width: 100%; border-collapse: collapse; font-size: .86rem; }}
thead th {{ text-align: left; font: 700 .62rem/1.3 var(--sans); letter-spacing: .08em; text-transform: uppercase; color: var(--faint); padding: .8rem .75rem; border-bottom: 1px solid var(--line); }}
tbody td {{ padding: .75rem; border-bottom: 1px solid var(--line-2); vertical-align: top; }}
tbody tr:last-child td {{ border-bottom: 0; }}
.cmp table {{ min-width: 720px; }}
.cmp td, .cmp th {{ text-align: center; }}
.cmp td:first-child, .cmp th:first-child {{ text-align: left; }}
.apexcol {{ background: rgba(201,162,39,0.08); }}
th.apexcol {{ color: var(--gold-deep); }}
.yes {{ color: var(--flow); font-weight: 700; }}
.no {{ color: var(--faint); }}
.part {{ color: var(--gold-deep); font-weight: 700; font-size: .76rem; }}
.catrow td {{ background: var(--page-2); font: 700 .62rem/1 var(--sans); letter-spacing: .1em; text-transform: uppercase; color: var(--faint); padding: .55rem .75rem; }}
.cx table {{ min-width: 640px; }}
.trust {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.6rem; }}
.tr {{ background: var(--card); border: 1px solid var(--line); border-top: 3px solid var(--gold); border-radius: var(--r); padding: 1.1rem 1.2rem; }}
.tr h3 {{ font-size: 1.02rem; }}
.tr p {{ margin-top: .45rem; font-size: .9rem; color: var(--muted); }}
@media (max-width: 900px) {{ .trust {{ grid-template-columns: 1fr; }} }}
.cx td {{ width: 50%; }}
.cx .src {{ display: block; margin-top: .3rem; font-size: .74rem; color: var(--faint); }}
.cx .ans {{ color: var(--flow); font-weight: 700; }}
.price table {{ min-width: 560px; }}
.price td.num, .price th.num {{ text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }}
.price tr.total td {{ background: var(--page-2); font-weight: 700; }}
.price tr.apex td {{ background: rgba(201,162,39,0.10); font-weight: 700; font-size: 1.02rem; }}
.price .big {{ color: var(--flow); }}
.note {{ margin-top: .9rem; font-size: .82rem; color: var(--faint); max-width: 70ch; }}
.note + .note {{ margin-top: .4rem; }}
footer {{ padding: 3rem 0 4rem; border-top: 1px solid var(--line); }}
footer .sig {{ font-weight: 700; letter-spacing: .04em; }}
footer p {{ font-size: .8rem; color: var(--faint); margin-top: .5rem; max-width: 80ch; }}
footer a {{ color: var(--faint); }}
@media (max-width: 900px) {{ .docs {{ grid-template-columns: 1fr; }} .minis {{ grid-template-columns: repeat(2, 1fr); }} .all ul {{ columns: 1; }} .doc .shot {{ height: 380px; }} }}
@media print {{
  @page {{ size: letter; margin: 0.45in; }}
  .lang, .pdf {{ display: none !important; }}
  body {{ font-size: 10.5pt; }}
  section {{ padding: 1.4rem 0; }}
  .hero {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .hero {{ padding: 2.6rem 0 2.4rem; min-height: 9.9in; display: flex; flex-direction: column; justify-content: center; }}
  .hero .logo {{ width: 90px; margin-bottom: 1rem; }}
  .hero h1 {{ font-size: 24pt; max-width: none; }}
  .stats {{ grid-template-columns: repeat(3, 1fr) !important; margin-top: 1rem; }}
  .docs {{ grid-template-columns: repeat(3, 1fr) !important; gap: .55rem; margin-top: 1rem; }}
  .doc {{ padding: .6rem; }}
  .doc h3 {{ font-size: 10.5pt; }}
  .doc .shot {{ height: 250px; }}
  .doc ul, .all ul {{ font-size: 7.6pt; }}
  .minis {{ grid-template-columns: repeat(4, 1fr) !important; gap: .55rem; }}
  .mini .shot {{ height: 130px; }}
  .mini figcaption {{ font-size: 7.4pt; }}
  .all ul {{ columns: 2 !important; }}
  .doc, .mini, .all, tr {{ break-inside: avoid; }}
  .tbl-wrap {{ overflow: visible; box-shadow: none; }}
  .cmp table, .cx table, .price table {{ min-width: 0; font-size: 8pt; }}
  tbody td {{ padding: .38rem .5rem; }}
  .shot .open {{ display: none; }}
  .sec-h h2 {{ font-size: 16pt; }}
  #docs {{ break-before: page; padding-top: 0; }}
  #complaints, #compare, #price {{ break-before: auto; padding: 1rem 0; }}
  .price .tbl-wrap {{ break-inside: avoid; }}
  .sec-h {{ break-after: avoid; }}
}}
</style>
</head>
<body>
<header class="hero">
  <div class="wrap">
    <img class="logo" src="../comparativo/apex-logo.png" alt="Apex">
    {t("Do lead à fatura, num sistema só.", "From lead to invoice, in one system.", "h1")}
    {t("Orçamento, contrato e fatura com a cara da empresa, enviados do celular do vendedor, sem digitar nada duas vezes.",
       "Estimate, contract and invoice in the business's own look, sent from the salesperson's phone, with nothing typed twice.", "p", "lede")}
    <div class="stats">
      <div class="stat"><div class="n">3 → 1</div>{t("Jobber, Joist e PandaDoc fazem, cada um, uma parte. O Apex faz tudo junto.", "Jobber, Joist and PandaDoc each do one part. Apex does it all together.", "p")}</div>
      <div class="stat"><div class="n">$406<small>{t("/mês", "/mo")}</small></div>{t("O que as três custam juntas para 5 usuários, e ainda sem os avisos da Flórida.", "What the three cost together for 5 users, still without the Florida notices.", "p")}</div>
      <div class="stat"><div class="n">$199<small>{t("/mês", "/mo")}</small></div>{t("Apex Completo: 5 usuários e tudo o que está nesta página.", "Apex Completo: 5 users and everything on this page.", "p")}</div>
    </div>
    <a class="pdf" href="{A}apex-sistema.pdf" target="_blank" rel="noopener">{t("Baixar em PDF", "Download as PDF")}</a>
  </div>
</header>

<section id="docs">
  <div class="wrap">
    <div class="sec-h">
      {t("Três documentos, um fluxo", "Three documents, one flow", "h2")}
      {t("Uma obra real de piscina, do orçamento ao pagamento do sinal. Clique em qualquer imagem para abrir o documento como o cliente vê.",
         "A real pool job, from the estimate to the deposit payment. Click any image to open the document the way the customer sees it.", "p")}
    </div>
    <div class="docs">
      {doc_col("estimate", "1 · Orçamento", "1 · Estimate", "O cliente escolhe a opção", "The customer picks the option", ESTIMATE)}
      {doc_col("contract", "2 · Contrato", "2 · Contract", "Assinado pelas duas partes", "Signed by both parties", CONTRACT)}
      {doc_col("invoice", "3 · Fatura", "3 · Invoice", "Cobrada por etapa", "Billed by stage", INVOICE)}
    </div>
    <div class="minis">
      {small("estimate", "whatsapp", "Como chega:", "How it arrives:", "o link no WhatsApp, com o logo da empresa.", "the link in WhatsApp, with the business logo.")}
      {small("receipt", "receipt", "Recibo:", "Receipt:", "sai sozinho a cada pagamento.", "issued on its own for every payment.")}
      {small("card", "card", "Cartão do vendedor:", "Salesperson card:", "o cliente salva no celular.", "the customer saves it to the phone.")}
      {small("referral", "referral", "Indicação:", "Referral:", "o amigo do cliente chega direto no vendedor.", "the customer's friend goes straight to the salesperson.")}
    </div>
    <div class="all">
      <p class="k">{t("Em todos os documentos", "On every document")}</p>
      {ul(ACROSS)}
    </div>
  </div>
</section>

<section class="tint" id="complaints">
  <div class="wrap">
    <div class="sec-h">
      {t("O que os usuários reclamam, e como o Apex resolve", "What users complain about, and how Apex answers", "h2")}
      {t("Reclamações reais de avaliações públicas de ferramentas do setor.", "Real complaints from public reviews of tools in this field.", "p")}
    </div>
    <div class="tbl-wrap cx"><table><thead><tr><th>{t("A reclamação", "The complaint")}</th><th>{t("No Apex", "In Apex")}</th></tr></thead><tbody>{complaints_rows}</tbody></table></div>
  </div>
</section>

<section id="legal">
  <div class="wrap">
    <div class="sec-h">
      {t("O que mais leva empreiteiros à Justiça na Flórida, e como o Apex protege", "What most often takes contractors to court in Florida, and how Apex protects them", "h2")}
      {t("43% dos donos de pequenas empresas já foram ameaçados ou envolvidos em um processo civil (U.S. Chamber ILR, 2013). Na construção, as brigas se repetem. Cada uma tem uma proteção pronta no sistema.",
         "43% of small-business owners have been threatened with or involved in a civil lawsuit (U.S. Chamber ILR, 2013). In construction the disputes repeat. Each one has a protection ready in the system.", "p")}
    </div>
    <div class="tbl-wrap cx"><table><thead><tr><th>{t("A disputa", "The dispute")}</th><th>{t("A proteção no Apex", "The protection in Apex")}</th></tr></thead><tbody>{legal_rows}</tbody></table></div>
    {t("As proteções organizam provas e prazos; não substituem um advogado. O texto dos avisos legais passa por revisão de advogado antes do uso.",
       "These protections organize evidence and deadlines; they do not replace an attorney. The legal notice text is reviewed by an attorney before use.", "p", "note")}
  </div>
</section>

<section class="tint" id="compare">
  <div class="wrap">
    <div class="sec-h">
      {t("O sistema inteiro, lado a lado", "The whole system, side by side", "h2")}
      {t("O que cada ferramenta faz, segundo a página do próprio fabricante.", "What each tool does, according to its own maker's page.", "p")}
    </div>
    {cmp_table()}
    {t("✕ quer dizer que o recurso não aparece na página de preços ou de recursos do fabricante, lida em 09/27/2026.",
       "✕ means the feature does not appear on the maker's pricing or feature page, read 09/27/2026.", "p", "note")}
  </div>
</section>

<section id="price">
  <div class="wrap">
    <div class="sec-h">
      {t("Quanto custa montar isso", "What it costs to assemble this", "h2")}
      {t("Com 5 usuários, na cobrança mensal sem fidelidade.", "With 5 users, on monthly billing with no commitment.", "p")}
    </div>
    <div class="tbl-wrap price"><table><thead><tr><th>{t("Ferramenta", "Tool")}</th><th>{t("Para quê", "What for")}</th><th class="num">{t("Por mês", "Per month")}</th></tr></thead><tbody>
      <tr><td><b>Jobber Connect</b> {t("(5 usuários)", "(5 users)")}</td><td>{t("Orçamentos, faturas, agenda e portal do cliente", "Estimates, invoices, scheduling and client portal")}</td><td class="num">$199</td></tr>
      <tr><td><b>Joist Elite</b></td><td>{t("Aditivos (change orders)", "Change orders")}</td><td class="num">$32</td></tr>
      <tr><td><b>PandaDoc Starter</b> {t("(5 usuários)", "(5 users)")}</td><td>{t("Criar contratos a partir de modelos e assinar", "Create contracts from templates and sign them")}</td><td class="num">$175</td></tr>
      <tr class="total"><td>{t("As três juntas", "All three together")}</td><td>{t("E ainda sem avisos da Flórida, proteção contra disputas ou consultor", "And still with no Florida notices, dispute protection or consultant")}</td><td class="num">$406</td></tr>
      <tr class="apex"><td>Apex Completo</td><td>{t("Tudo desta página, 5 usuários inclusos", "Everything on this page, 5 users included")}</td><td class="num big">$199</td></tr>
    </tbody></table></div>
    {t("Preços publicados pelos fabricantes, lidos em 09/27 e 09/28/2026, cobrança mensal sem fidelidade. Jobber Connect: opções no orçamento, custo da obra e pipeline custam +$100/mês (Grow) ou +$300/mês (Plus); a oferta de desconto dele termina em 09/30. PandaDoc Starter aceita até 5 modelos; modelos ilimitados e cobrança on-line custam +$150/mês (Business). O Joist não publica quantos usuários cada plano inclui. No plano anual, todos ficam mais baratos, o Apex também.", "Prices published by the makers, read 09/27 and 09/28/2026, monthly billing with no commitment. Jobber Connect: estimate options, job costing and the pipeline cost +$100/mo (Grow) or +$300/mo (Plus); its discount offer ends 09/30. PandaDoc Starter allows up to 5 templates; unlimited templates and online payment collection cost +$150/mo (Business). Joist does not publish how many users each plan includes. On annual billing all of them cost less, Apex included.", "p", "note")}
    {t("Fontes: getjobber.com/pricing, joist.com/pricing, pandadoc.com/pricing.", "Sources: getjobber.com/pricing, joist.com/pricing, pandadoc.com/pricing.", "p", "note")}
  </div>
</section>

<footer>
  <div class="wrap">
    <p class="sig">RAFAEL PRATA · Founder &amp; CEO, APEX Business &amp; Leadership · 09/28/2026</p>
    {t("A empresa, o cliente e os valores dos documentos são um exemplo de demonstração.", "The business, the customer and the document amounts are a demonstration example.", "p")}
  </div>
</footer>

<script>
(function () {{
  'use strict';
  var KEY = 'fluxo-lang';
  function get() {{ try {{ var s = localStorage.getItem(KEY); if (s === 'en' || s === 'pt') return s; }} catch (e) {{}} var q = new URLSearchParams(location.search).get('lang'); return q === 'en' ? 'en' : 'pt'; }}
  function set(lang) {{
    document.documentElement.setAttribute('lang', lang === 'pt' ? 'pt-BR' : 'en');
    try {{ localStorage.setItem(KEY, lang); }} catch (e) {{}}
    document.querySelectorAll('[data-pt]').forEach(function (el) {{ var t = lang === 'pt' ? el.dataset.pt : el.dataset.en; if (t !== undefined) el.innerHTML = t; }});
    document.querySelectorAll('.lang button').forEach(function (b) {{ b.setAttribute('aria-pressed', String(b.dataset.l === lang)); }});
  }}
  var n = document.createElement('div'); n.className = 'lang'; n.setAttribute('role', 'group'); n.setAttribute('aria-label', 'Idioma / Language');
  n.innerHTML = '<button type="button" data-l="pt" aria-pressed="false">PT</button><button type="button" data-l="en" aria-pressed="false">EN</button>';
  n.addEventListener('click', function (e) {{ var b = e.target.closest('button[data-l]'); if (b) set(b.dataset.l); }});
  document.body.appendChild(n);
  set(new URLSearchParams(location.search).get('lang') || get());
}})();
</script>
</body>
</html>
'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write(PAGE)
print("wrote", OUT, len(PAGE))
