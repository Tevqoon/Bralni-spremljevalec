# Bralni spremljevalec

Bralni spremljevalec je program, ki uporabniku omogoča spremljanje
branih knjig in čas, ki ga potrebuje zanje.

## Delovanje

Omogoča dodajanje knjig in branja posamezne knjige, iz porabljenega časa 
in prebranih strani izračuna povprečno hitrost branja za dano knjigo 
in ponuja čas, ki ga bi uporabnik potreboval da prebere preostanek dela, 
z isto povprečno hitrostjo.

Hkrati omogoča filtriranje knjižnice glede na avtorja, kategorijo knjige,
ter trenutno stanje branja (nezačeto, začeto in prebrano). Za filtrirano
skupino potem punuja skupno statistiko časa in napredka. 

## Zagon

Program zaženemo iz terminala z `python3 spletni_vmesnik.py`. Le-ta zažene spletni vmesnik,
ki se nahaja na `http://127.0.0.1:8080`. Ustvarimo uporabniški račun in se prijavimo.
Z zavihkom "Dodaj knjigo" dodamo poljubne knjige, nakar lahko začnemo uporabljati
program.

## Navodila za uporabo

Ko dodamo knjige, jih lahko v spodnjem levem meniju izberemo. To nas prinese do pogleda
na posamezno knjigo. Tam lahko spremenimo podatke knjige, jo izbrišemo, ali pa dodamo 
novo branje, kjer označimo čas branja in zadnjo doseženo stran. Ta branja so glavni način
kako programu povemo, koliko smo brali. Podatke lahko poljubno urejamo v urejevalnem
zavihku. 

Ko imamo nekaj knjig lahko z zgornjim levim menijem izbiramo filtre. Le-ti nam omogočajo
večjo preglednost nad knjižnico, ker nam omogočajo, da se omejimo le na podmnožico knjig,
ki jih imao v knjižnici. S klikom na zavihke "Avtorji," "Kategorije" in "Stanja" se
odločamo kakšne knjige želimo. Ko se za nek zavihek odločimo, katero kombinacijo
avtorjev, kategorij ali stanj želimo, kliknemo na določi filtre, kar našo odločitev shrani ter nam omogoči, da se premaknemo na drugo kategorijo. Z gumbom "Ponastavi filtre",
pričakovani, ponastavimo filtre in zopet prikažemo celotno knjižnico.

Če kliknemo na zavihek "Stanje knjižnice", nam le-ta za filtrirano skupino (v posebnem
primeru celotno knjižnico) prikaže naš napredek. Hkrati za vsako vizualno predstavi
kako daleč smo prišli z branjem.

Ko ste končali z uporabo programa, se odjavite z zgornjim levim gumbom. Vaše spremembe
in uporaba programa se avtomatično sproti shranjajo.

## Možne izboljšave in opombe
* Priložen je tudi tekstovni vmesnik, a ta zaradi majhnih sprememb v modelu po njegovi zasnovi ni 100% podprt. Le-ta ima načrtovano drugo verzijo, ki bo omogočala integracijo z 
Unixovim pipelineom.
* Program potrebuje priložen `bottle.py`.
* Z relativno majhnimi spremembami modela bi se program dalo posplošiti na več možnosti, kot samo knjige
* Možnost večih kategorij in avtorjev na knjigo.
* Spletna štoparica, s katero bi lahko kar na spletni strani pogledali, koliko časa je trajala
dana seansa branja.
* Omogočanje eksportiranja posameznih knjig in celih knjižnic na dober način.
* Omogočanje večih knjižnih polic na posamezen račun.
* Importiranje novih knjig direktno iz strani, kot so Google books.
* Shranjevanje posameznih branj in natančnejša analiza, ki bi potencialno omogočila
izračun optimalne količine branja glede na dolžino.
* Podatki iz prejšnje alineje bi potem lahko pripomogli k načrtu branja.
* Integracija prejšnje točke z uporabnikovim spletnim koledarjem
* ...