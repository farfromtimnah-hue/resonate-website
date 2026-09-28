#!/usr/bin/env python3
"""Builds resonate-website/public/fluxo/sistema/pdf.html: the pitch as FIXED
SLIDES, the same shell as apex-command-center/templates/client-invoice-template.html
(7.5in x 10in slides inside Letter with 0.5in margins, footer inside the slide,
break-after: page). Portuguese. A built-in check marks any slide whose content
runs into the footer zone (data-overflow="1")."""
import os, runpy, html
here = os.path.dirname(os.path.abspath(__file__))
bp = runpy.run_path(os.path.join(here, "build_page.py"))  # reuse the same texts (also rewrites index.html, unchanged)
A, DOC = bp["A"], bp["DOC"]
OUT = os.path.expanduser("~/resonate-website/public/fluxo/sistema/pdf.html")
TOTAL = 11

def e(s): return html.escape(s, quote=False)
def ul(items): return "<ul>" + "".join(f"<li>{e(pt)}</li>" for pt, _ in items) + "</ul>"

def slide(n, body, cls="", footer=True):
    ft = f'<div class="ft"><span>APEX Business &amp; Leadership</span><span>{n} / {TOTAL}</span></div>' if footer else ""
    return f'<section class="slide {cls}"><div class="content">{body}</div>{ft}</section>'

def doc_slide(n, key, k, h, lede, items):
    return slide(n, f'''<p class="k">{e(k)}</p><h2>{e(h)}</h2><p class="lede">{e(lede)}</p>
<div class="two"><a class="shot tall" href="{DOC[key]}"><img src="{A}{key}.jpg" alt=""></a>
<div class="feat">{ul(items)}<p class="linkline">Abrir o documento real: <a href="{DOC[key]}">{e(DOC[key].replace("https://", ""))}</a></p></div></div>''')

Y, N = '<span class="yes">✓</span>', '<span class="no">✕</span>'
def cell(v):
    if v == bp["Y"]: return Y
    if v == bp["N"]: return N
    return v  # partial: already a span with data-pt; strip to PT text
import re
def pt_only(s): return re.sub(r'<span data-pt="([^"]*)"[^>]*>.*?</span>', lambda m: html.unescape(m.group(1)), s)

rows = []
for r in bp["ROWS"]:
    if r[0] == "cat": rows.append(f'<tr class="cat"><td colspan="5">{e(r[1])}</td></tr>')
    else: rows.append(f'<tr><td>{e(r[0])}</td><td class="apexcol">{Y}</td>' + "".join(f"<td>{pt_only(cell(v))}</td>" for v in r[2:5]) + '</tr>')
cut = next(i for i, r in enumerate(bp["ROWS"]) if r[0] == "cat" and r[1] == "Contra disputas")
HEAD = '<table class="cmp"><thead><tr><th>Recurso</th><th class="apexcol">Apex</th><th>Jobber</th><th>Joist</th><th>PandaDoc</th></tr></thead><tbody>'
cmp1 = HEAD + "".join(rows[:cut]) + "</tbody></table>"
cmp2 = HEAD + "".join(rows[cut:]) + "</tbody></table>"
legal = "".join(f'<tr><td>{e(a)}<span class="src">{e(sp)}</span></td><td class="ans">{e(c)}</td></tr>' for a, b, sp, se, c, d in bp["LEGAL"])

cx = "".join(f'<tr><td>{e(a)}<span class="src">{e(sp)}</span></td><td class="ans">{e(c)}</td></tr>' for a, b, sp, se, u, c, d in bp["COMPLAINTS"])

S = []
S.append(slide(1, f'''<img class="cover-logo" src="../comparativo/apex-logo.png" alt="Apex">
<h1>Do lead à fatura,<br>num sistema só.</h1>
<p class="cover-line">Orçamento, contrato e fatura com a cara da empresa, enviados do celular do vendedor.</p>
<p class="cover-web">resonateai.online</p>''', "cover", footer=False))
S.append(slide(2, f'''<p class="k">Em resumo</p><h2>Três ferramentas viram uma.</h2>
<div class="stats"><div class="stat"><div class="n">3 → 1</div><p>Jobber, Joist e PandaDoc fazem, cada um, uma parte. O Apex faz tudo junto.</p></div>
<div class="stat"><div class="n">$406<small>/mês</small></div><p>O que as três custam juntas para 5 usuários, e ainda sem os avisos da Flórida.</p></div>
<div class="stat gold"><div class="n">$199<small>/mês</small></div><p>Apex Completo: 5 usuários e tudo o que está neste documento.</p></div></div>
<h3 class="sub">O fluxo</h3>
<div class="flow"><div><b>Lead</b><span>chega com nome, telefone e serviço</span></div><div><b>Orçamento</b><span>Best, Better e Good; o cliente escolhe e assina</span></div><div><b>Contrato</b><span>avisos da Flórida por regra; as duas partes assinam</span></div><div><b>Projeto</b><span>criado sozinho quando o cliente aceita</span></div><div><b>Fatura</b><span>por etapa, com recibo a cada pagamento</span></div></div>
<p class="big-note">Nada é digitado duas vezes. Cada etapa já nasce com os dados da anterior.</p>'''))
S.append(doc_slide(3, "estimate", "1 · Orçamento", "O cliente escolhe a opção", "Três opções, da maior para a menor. O cliente escolhe e assina no celular, sem criar conta.", bp["ESTIMATE"]))
S.append(doc_slide(4, "contract", "2 · Contrato", "Assinado pelas duas partes", "Nasce do orçamento aceito, com os avisos da Flórida aplicados por regra.", bp["CONTRACT"]))
S.append(doc_slide(5, "invoice", "3 · Fatura", "Cobrada por etapa", "Uma fatura por etapa, com o saldo do contrato sempre à vista.", bp["INVOICE"]))
minis = "".join(f'<figure><a class="shot mini" href="{DOC[k]}"><img src="{A}{img}.jpg" alt=""></a><figcaption><b>{e(a)}</b> {e(b)}</figcaption></figure>' for k, img, a, b in [
    ("estimate", "whatsapp", "Como chega:", "o link no WhatsApp, com o logo da empresa."),
    ("receipt", "receipt", "Recibo:", "sai sozinho a cada pagamento."),
    ("card", "card", "Cartão do vendedor:", "o cliente salva no celular."),
    ("referral", "referral", "Indicação:", "o amigo do cliente chega direto no vendedor.")])
S.append(slide(6, f'''<p class="k">O que acompanha</p><h2>Como chega ao cliente</h2><div class="minis">{minis}</div>
<div class="all"><p class="k">Em todos os documentos</p>{ul(bp["ACROSS"])}</div>'''))
S.append(slide(7, f'''<p class="k">Avaliações públicas</p><h2>O que os usuários reclamam, e como o Apex resolve</h2><p class="lede">Reclamações reais de avaliações públicas de ferramentas do setor.</p>
<table class="cx"><thead><tr><th>A reclamação</th><th>No Apex</th></tr></thead><tbody>{cx}</tbody></table>'''))
S.append(slide(8, f'''<p class="k">Proteção</p><h2>O que mais leva empreiteiros à Justiça na Flórida, e como o Apex protege</h2>
<p class="lede">43% dos donos de pequenas empresas já foram ameaçados ou envolvidos em um processo civil (U.S. Chamber ILR, 2013). Na construção, as brigas se repetem.</p>
<table class="cx"><thead><tr><th>A disputa</th><th>A proteção no Apex</th></tr></thead><tbody>{legal}</tbody></table>
<p class="note">As proteções organizam provas e prazos; não substituem um advogado. O texto dos avisos legais passa por revisão de advogado antes do uso.</p>'''))
S.append(slide(9, f'''<p class="k">Lado a lado</p><h2>O sistema inteiro (1 de 2)</h2>{cmp1}
<p class="note">✕ quer dizer que o recurso não aparece na página de preços ou de recursos do fabricante, lida em 09/27/2026.</p>'''))
S.append(slide(10, f'''<p class="k">Lado a lado</p><h2>O sistema inteiro (2 de 2)</h2>{cmp2}'''))
S.append(slide(11, f'''<p class="k">Custo mensal</p><h2>Quanto custa montar isso</h2><p class="lede">Com 5 usuários, na cobrança mensal sem fidelidade.</p>
<table class="price"><thead><tr><th>Ferramenta</th><th>Para quê</th><th class="num">Por mês</th></tr></thead><tbody>
<tr><td><b>Jobber Connect</b> (5 usuários)</td><td>Orçamentos, faturas, agenda e portal do cliente</td><td class="num">$199</td></tr>
<tr><td><b>Joist Elite</b></td><td>Aditivos (change orders)</td><td class="num">$32</td></tr>
<tr><td><b>PandaDoc Starter</b> (5 usuários)</td><td>Criar contratos a partir de modelos e assinar</td><td class="num">$175</td></tr>
<tr class="total"><td>As três juntas</td><td>E ainda sem avisos da Flórida, proteção contra disputas ou consultor</td><td class="num">$406</td></tr>
<tr class="apex"><td>Apex Completo</td><td>Tudo deste documento, 5 usuários inclusos</td><td class="num">$199</td></tr></tbody></table>
<p class="note">Preços publicados pelos fabricantes, lidos em 09/27 e 09/28/2026, cobrança mensal sem fidelidade. Jobber Connect: opções no orçamento, custo da obra e pipeline custam +$100/mês (Grow) ou +$300/mês (Plus); a oferta de desconto dele termina em 09/30. PandaDoc Starter aceita até 5 modelos; modelos ilimitados e cobrança on-line custam +$150/mês (Business). O Joist não publica quantos usuários cada plano inclui. No plano anual, todos ficam mais baratos, o Apex também.</p>
<p class="note">Fontes: getjobber.com/pricing, joist.com/pricing, pandadoc.com/pricing.</p>
<p class="note">A empresa, o cliente e os valores dos documentos são um exemplo de demonstração.</p>
<div class="sig">RAFAEL PRATA · Founder &amp; CEO, APEX Business &amp; Leadership · 09/28/2026</div>'''))

PAGE = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=816">
<meta name="robots" content="noindex, nofollow">
<title>Apex · Do lead à fatura (PDF)</title>
<style>
/* Same shell as apex-command-center/templates/client-invoice-template.html:
   fixed 7.5in x 10in slides, footer inside the slide, Letter with 0.5in margins. */
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{ --ink:#14171C; --muted:#5A6270; --faint:#8B93A0; --rule:#E3E7EC; --navy:#0F1E3D; --gold:#C9A227; --gold-deep:#8A6F2C; --flow:#3f7d4e; --pad-x:0.45in; --pad-top:0.45in; --pad-bottom:0.8in; }}
html, body {{ background:#e9ebee; }}
body {{ font-family:"Helvetica Neue", Helvetica, Arial, sans-serif; color:var(--ink); font-size:10pt; line-height:1.4; padding:24px 0; }}
.slide {{ position:relative; width:7.5in; height:10in; margin:0 auto 24px; background:#fff; padding:var(--pad-top) var(--pad-x) var(--pad-bottom); overflow:hidden; box-shadow:0 2px 14px rgba(0,0,0,0.12); }}
.slide .content {{ height:100%; }}
.ft {{ position:absolute; left:var(--pad-x); right:var(--pad-x); bottom:.32in; display:flex; justify-content:space-between; font-size:8pt; color:var(--muted); border-top:1px solid var(--rule); padding-top:.12in; }}
.slide[data-overflow="1"] {{ outline:4px solid #c00; }}
.k {{ font-size:7.5pt; font-weight:700; letter-spacing:.12em; text-transform:uppercase; color:var(--gold-deep); }}
h1, h2, h3 {{ letter-spacing:-0.01em; line-height:1.15; }}
h2 {{ font-size:20pt; margin-top:.08in; }}
.lede {{ margin-top:.08in; color:var(--muted); font-size:10.5pt; }}
/* cover: one solid navy field, edge to edge (Rafa's cover rule) */
.cover {{ background:var(--navy); color:#fff; padding:0; }}
.cover .content {{ display:flex; flex-direction:column; justify-content:center; padding:0 .8in; }}
.cover-logo {{ width:1.6in; height:auto; display:block; margin-bottom:.5in; }}
.cover h1 {{ font-size:36pt; }}
.cover-line {{ margin-top:.25in; font-size:14pt; color:rgba(255,255,255,.8); max-width:5in; }}
.cover-web {{ margin-top:.6in; font-size:10pt; color:var(--gold); letter-spacing:.06em; }}
.stats {{ display:grid; grid-template-columns:repeat(3,1fr); gap:.14in; margin-top:.3in; }}
.stat {{ border:1px solid var(--rule); border-radius:8pt; padding:.14in; }}
.stat .n {{ font-size:22pt; font-weight:700; color:var(--navy); }}
.stat .n small {{ font-size:9pt; color:var(--muted); font-weight:400; }}
.stat.gold {{ background:var(--navy); border-color:var(--navy); color:#fff; }}
.stat.gold .n {{ color:var(--gold); }} .stat.gold .n small, .stat.gold p {{ color:rgba(255,255,255,.8); }}
.stat p {{ margin-top:.05in; font-size:9pt; color:var(--muted); }}
.sub {{ margin-top:.45in; font-size:12pt; }}
.flow {{ display:grid; grid-template-columns:repeat(5,1fr); gap:.08in; margin-top:.14in; }}
.flow div {{ border-top:3px solid var(--gold); padding-top:.08in; font-size:8.5pt; color:var(--muted); }}
.flow b {{ display:block; font-size:10pt; color:var(--ink); margin-bottom:.03in; }}
.big-note {{ margin-top:.45in; font-size:13pt; font-weight:700; color:var(--navy); max-width:5.5in; }}
.two {{ display:grid; grid-template-columns:3.3in 1fr; gap:.25in; margin-top:.22in; }}
.shot {{ display:block; border:1px solid var(--rule); border-radius:6pt; overflow:hidden; background:#fff; }}
.shot img {{ width:100%; height:auto; display:block; }}
.shot.tall {{ max-height:7.2in; align-self:start; }}
.feat ul {{ padding-left:.16in; font-size:9.5pt; color:var(--ink); }}
.feat li {{ margin-bottom:.09in; }}
.linkline {{ margin-top:.18in; font-size:8pt; color:var(--muted); word-break:break-all; }}
.linkline a {{ color:var(--gold-deep); }}
.minis {{ display:grid; grid-template-columns:repeat(4,1fr); gap:.12in; margin-top:.22in; }}
.minis figure {{ margin:0; }}
.shot.mini {{ max-height:2.3in; }}
figcaption {{ margin-top:.06in; font-size:8pt; color:var(--muted); }}
figcaption b {{ color:var(--ink); }}
.all {{ margin-top:.3in; border-left:3px solid var(--gold); padding:.12in .18in; background:#faf9f6; border-radius:6pt; }}
.all ul {{ margin-top:.08in; padding-left:.16in; columns:2; column-gap:.3in; font-size:8.8pt; }}
.all li {{ margin-bottom:.07in; break-inside:avoid; }}
table {{ width:100%; border-collapse:collapse; margin-top:.2in; font-size:8.6pt; }}
th {{ text-align:left; font-size:7pt; letter-spacing:.08em; text-transform:uppercase; color:var(--faint); padding:.06in; border-bottom:1px solid var(--rule); }}
td {{ padding:.06in; border-bottom:1px solid #f0f1f3; vertical-align:top; }}
.cx td {{ width:50%; }} .cx .src {{ display:block; margin-top:.03in; font-size:7.3pt; color:var(--faint); }} .cx .ans {{ color:var(--flow); font-weight:700; }}
.cmp td, .cmp th {{ text-align:center; }} .cmp td:first-child, .cmp th:first-child {{ text-align:left; }}
.cmp tr.cat td {{ background:#f5f4f0; font-size:6.8pt; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--faint); padding:.04in .06in; }}
.cmp td {{ padding:.035in .06in; font-size:8.1pt; }}
.apexcol {{ background:rgba(201,162,39,.09); }} th.apexcol {{ color:var(--gold-deep); }}
.yes {{ color:var(--flow); font-weight:700; }} .no {{ color:var(--faint); }}
.part {{ color:var(--gold-deep); font-weight:700; font-size:7.4pt; }}
.price td.num, .price th.num {{ text-align:right; white-space:nowrap; }}
.price td {{ font-size:9.5pt; padding:.09in .06in; }}
.price tr.total td {{ background:#f5f4f0; font-weight:700; }}
.price tr.apex td {{ background:var(--navy); color:#fff; font-weight:700; font-size:11pt; }}
.price tr.apex td.num {{ color:var(--gold); }}
.note {{ margin-top:.14in; font-size:8pt; color:var(--muted); }}
.trust {{ display:grid; grid-template-columns:1fr; gap:.18in; margin-top:.35in; }}
.tr {{ border:1px solid var(--rule); border-top:3px solid var(--gold); border-radius:8pt; padding:.2in .24in; }}
.tr h3 {{ font-size:14pt; color:var(--navy); }}
.tr p {{ margin-top:.08in; font-size:11pt; color:var(--muted); }}
.sig {{ position:absolute; left:var(--pad-x); right:var(--pad-x); bottom:.95in; font-size:8.5pt; font-weight:700; letter-spacing:.05em; color:var(--navy); }}
@media print {{
  body {{ background:#fff; padding:0; }}
  .slide {{ width:7.5in; height:9.98in; margin:0; box-shadow:none; break-after:page; page-break-after:always; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
  .slide:last-child {{ break-after:auto; page-break-after:auto; }}
  .slide[data-overflow="1"] {{ outline:none; }}
  @page {{ size:Letter portrait; margin:0.5in; }}
}}
</style>
</head>
<body>
{"".join(S)}
<script>
// Overflow check: content must end above the footer zone of its own slide.
function checkSlides() {{
  var bad = [];
  document.querySelectorAll('.slide').forEach(function (s, i) {{
    var limit = s.getBoundingClientRect().bottom - 0.8 * 96;
    var over = false;
    s.querySelectorAll('.content *').forEach(function (el) {{ if (el.closest('.sig')) return; var r = el.getBoundingClientRect(); if (r.height && r.bottom > limit + 1) over = true; }});
    s.setAttribute('data-overflow', over ? '1' : '0'); if (over) bad.push(i + 1);
  }});
  document.body.setAttribute('data-overflow-slides', bad.join(','));
  document.body.setAttribute('data-render-done', '1');
}}
window.addEventListener('load', function () {{ setTimeout(checkSlides, 300); }});
</script>
</body>
</html>
'''
open(OUT, "w").write(PAGE)
print("wrote", OUT, len(PAGE))
