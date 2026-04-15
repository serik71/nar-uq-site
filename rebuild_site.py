#!/usr/bin/env python3
import os, shutil

BASE = '/tmp/nar-uq-site2'
os.chdir(BASE)

# ── 1. Очищаем мусор ─────────────────────────────────────────────────────────
for bad in ['content/content', 'layouts/layouts', 'layouts/monographs',
            'fix_site.py', 'single.html', 'style.css']:
    if os.path.isdir(bad):
        shutil.rmtree(bad)
        print(f'Removed dir: {bad}')
    elif os.path.isfile(bad):
        os.remove(bad)
        print(f'Removed file: {bad}')

# ── 2. Структура папок ───────────────────────────────────────────────────────
for d in [
    'layouts/_default',
    'layouts/partials',
    'content/ru/monographs',
    'static/css',
    'i18n',
]:
    os.makedirs(d, exist_ok=True)

# ── 3. hugo.toml ─────────────────────────────────────────────────────────────
with open('hugo.toml', 'w') as f:
    f.write('''baseURL = "https://nar-uq.org/"
languageCode = "ru"
title = "NAR-UQ"
defaultContentLanguage = "ru"
defaultContentLanguageInSubdir = true

[languages]
  [languages.ru]
    languageName = "RU"
    weight = 1
    title = "NAR-UQ — Словесность"
  [languages.en]
    languageName = "EN"
    weight = 2
    title = "NAR-UQ — Wordry"
  [languages.kk]
    languageName = "KK"
    weight = 3
    title = "NAR-UQ — Сөздік"

[params]
  description = "Словесность без посредников"
  author = "Серик Болатжанович Рысжанов"
  accentColor = "#1a6b6b"
''')
print('hugo.toml OK')

# ── 4. layouts/_default/baseof.html ──────────────────────────────────────────
with open('layouts/_default/baseof.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<html lang="{{ .Lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ .Title }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    {{ partial "header.html" . }}
    <main>
        {{ block "main" . }}{{ end }}
    </main>
    {{ partial "footer.html" . }}
</body>
</html>
''')
print('baseof.html OK')

# ── 5. layouts/_default/single.html ──────────────────────────────────────────
with open('layouts/_default/single.html', 'w') as f:
    f.write('''{{ define "main" }}
<article style="padding: 140px 40px 80px; max-width: 1200px; margin: 0 auto;">
    <h1 style="font-family: \'Playfair Display\',serif; font-size: 3rem; color: #1a6b6b; margin-bottom: 2rem;">{{ .Title }}</h1>
    <div style="font-size: 1.1rem; line-height: 1.9; color: #343a40;">
        {{ .Content }}
    </div>
</article>
{{ end }}
''')
print('single.html OK')

# ── 6. layouts/_default/list.html ────────────────────────────────────────────
with open('layouts/_default/list.html', 'w') as f:
    f.write('''{{ define "main" }}
<article style="padding: 140px 40px 80px; max-width: 1200px; margin: 0 auto;">
    <h1 style="font-family: \'Playfair Display\',serif; font-size: 3rem; color: #1a6b6b; margin-bottom: 2rem;">{{ .Title }}</h1>
    <div style="font-size: 1.1rem; line-height: 1.9; color: #343a40;">
        {{ .Content }}
    </div>
</article>
{{ end }}
''')
print('list.html OK')

# ── 7. layouts/partials/header.html ──────────────────────────────────────────
with open('layouts/partials/header.html', 'w') as f:
    f.write('''<header>
    <div class="header-inner">
        <a href="/{{ .Lang }}/" class="logo">
            <img class="logo-mark" src="/logo.png" alt="NQ">
            <span class="logo-text">NAR-UQ</span>
        </a>
        <nav>
            <a href="/{{ .Lang }}/topics/">{{ i18n "menuTopics" | default "Темы" }}</a>
            <span class="nav-inactive">{{ i18n "menuTranslation" | default "Перевод" }}<span class="nav-soon">Готовится</span></span>
            <span class="nav-inactive">{{ i18n "menuArticles" | default "Статьи" }}<span class="nav-soon">Готовится</span></span>
            <a href="/{{ .Lang }}/monographs/">{{ i18n "menuMonographs" | default "Монографии" }}</a>
            <span class="nav-inactive">{{ i18n "menuLearning" | default "Обучение" }}<span class="nav-soon">Готовится</span></span>
            <span class="nav-inactive">{{ i18n "menuAnalytics" | default "Аналитика" }}<span class="nav-soon">Готовится</span></span>
            <span class="nav-inactive">{{ i18n "menuDistribution" | default "Распространение" }}<span class="nav-soon">Готовится</span></span>
            <a href="/{{ .Lang }}/about/">{{ i18n "menuAbout" | default "О проекте" }}</a>
            <span class="nav-inactive">{{ i18n "menuContacts" | default "Контакты" }}<span class="nav-soon">Готовится</span></span>
            <div class="lang-switcher">
                <a href="/ru/" {{ if eq .Lang "ru" }}class="active"{{ end }}>RU</a>
                <a href="/en/" {{ if eq .Lang "en" }}class="active"{{ end }}>EN</a>
                <a href="/kk/" {{ if eq .Lang "kk" }}class="active"{{ end }}>KK</a>
            </div>
        </nav>
    </div>
</header>
''')
print('header.html OK')

# ── 8. layouts/partials/footer.html ──────────────────────────────────────────
with open('layouts/partials/footer.html', 'w') as f:
    f.write('''<footer>
    <div class="footer-inner">
        <div class="footer-logo">
            <img src="/logo.png" alt="NQ">
            <span>NAR-UQ</span>
        </div>
        <div class="footer-copy">© 2026 {{ .Site.Params.author }}</div>
        <div class="footer-contact">
            <a href="/{{ .Lang }}/contact/">{{ i18n "contact" | default "Связаться" }}</a>
        </div>
    </div>
</footer>
''')
print('footer.html OK')

# ── 9. layouts/partials/index.html (главная) ─────────────────────────────────
with open('layouts/partials/index.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<html lang="{{ .Lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="facebook-domain-verification" content="z58zq8skkkxsy43x5niikfcob49b0w" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ .Site.Title }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <div class="header-inner">
            <a href="/{{ .Lang }}/" class="logo">
                <img class="logo-mark" src="/logo.png" alt="NQ">
                <span class="logo-text">NAR-UQ</span>
            </a>
            <nav>
                <a href="/{{ .Lang }}/topics/">{{ i18n "menuTopics" | default "Темы" }}</a>
                <span class="nav-inactive">{{ i18n "menuTranslation" | default "Перевод" }}<span class="nav-soon">Готовится</span></span>
                <span class="nav-inactive">{{ i18n "menuArticles" | default "Статьи" }}<span class="nav-soon">Готовится</span></span>
                <a href="/{{ .Lang }}/monographs/">{{ i18n "menuMonographs" | default "Монографии" }}</a>
                <span class="nav-inactive">{{ i18n "menuLearning" | default "Обучение" }}<span class="nav-soon">Готовится</span></span>
                <span class="nav-inactive">{{ i18n "menuAnalytics" | default "Аналитика" }}<span class="nav-soon">Готовится</span></span>
                <span class="nav-inactive">{{ i18n "menuDistribution" | default "Распространение" }}<span class="nav-soon">Готовится</span></span>
                <a href="/{{ .Lang }}/about/">{{ i18n "menuAbout" | default "О проекте" }}</a>
                <span class="nav-inactive">{{ i18n "menuContacts" | default "Контакты" }}<span class="nav-soon">Готовится</span></span>
                <div class="lang-switcher">
                    <a href="/ru/" {{ if eq .Lang "ru" }}class="active"{{ end }}>RU</a>
                    <a href="/en/" {{ if eq .Lang "en" }}class="active"{{ end }}>EN</a>
                    <a href="/kk/" {{ if eq .Lang "kk" }}class="active"{{ end }}>KK</a>
                </div>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="hero-content">
            <div class="hero-badge">{{ i18n "heroBadge" | default "Реформа понимания" }}</div>
            <h1 class="hero-title">{{ i18n "heroTitle1" | default "Словесность" }}<br><span class="highlight">{{ i18n "heroTitle2" | default "без посредников" }}</span></h1>
            <p class="hero-subtitle">{{ i18n "heroSubtitle" | default "Послание самодостаточно." }}</p>
            <div class="hero-buttons">
                <a href="/{{ .Lang }}/translation/" class="btn btn-primary">{{ i18n "btnTranslation" | default "Читать перевод" }} →</a>
            </div>
            <div class="hero-stats">
                <div class="stat"><div class="stat-number">114</div><div class="stat-label">{{ i18n "statChapters" | default "глав перевода" }}</div></div>
                <div class="stat"><div class="stat-number">150+</div><div class="stat-label">{{ i18n "statArticles" | default "тематических статей" }}</div></div>
                <div class="stat"><div class="stat-number">25+</div><div class="stat-label">{{ i18n "statYears" | default "лет исследований" }}</div></div>
            </div>
        </div>
        <div class="hero-visual">
            <div class="orbit-ring orbit-ring-1"></div>
            <div class="orbit-ring orbit-ring-2"></div>
            <div class="orbit-ring orbit-ring-3"></div>
            <div class="orbit-core"><img src="/logo.png" alt="NAR-UQ"></div>
            <div class="orbit-item orbit-item-1"><div class="orbit-pill">{{ i18n "menuTranslation" | default "Перевод" }}</div></div>
            <div class="orbit-item orbit-item-2"><div class="orbit-pill">{{ i18n "menuMonographs" | default "Монографии" }}</div></div>
            <div class="orbit-item orbit-item-3"><div class="orbit-pill">{{ i18n "menuArticles" | default "Статьи" }}</div></div>
            <div class="orbit-item orbit-item-4"><div class="orbit-pill">{{ i18n "menuAnalytics" | default "Аналитика" }}</div></div>
            <div class="orbit-item orbit-item-5"><div class="orbit-pill">{{ i18n "menuLearning" | default "Обучение" }}</div></div>
            <div class="orbit-item orbit-item-6"><div class="orbit-pill">{{ i18n "menuDistribution" | default "Распространение" }}</div></div>
            <div class="orbit-item orbit-item-7"><div class="orbit-pill">{{ i18n "menuAbout" | default "О проекте" }}</div></div>
        </div>
    </section>

    <section class="manifesto">
        <div class="manifesto-inner">
            <div class="manifesto-label">{{ i18n "manifestoLabel" | default "Позиция проекта" }}</div>
            <h2 class="manifesto-title">{{ i18n "manifestoTitle" | default "Доверие первоисточнику" }}</h2>
            <p class="manifesto-text">{{ i18n "manifestoText1" | default "Лишь Творец объективен, а люди субъективны." }} <strong>{{ i18n "manifestoStrong1" | default "1400 лет традиции" }}</strong> {{ i18n "manifestoText2" | default "увели от откровения." }}<br><br>{{ i18n "manifestoText3" | default "Этот проект предлагает" }} <strong>{{ i18n "manifestoStrong2" | default "альтернативу" }}</strong>{{ i18n "manifestoText4" | default ": понимание Словесности из самой Словесности." }}</p>
        </div>
    </section>

    <section class="features">
        <div class="features-inner">
            <div class="features-header">
                <div class="section-label">{{ i18n "featuresLabel" | default "Разделы" }}</div>
                <h2 class="section-title">{{ i18n "featuresTitle" | default "Что вы найдёте на сайте" }}</h2>
            </div>
            <div class="features-grid">
                <a href="/{{ .Lang }}/translation/" class="feature-card"><div class="feature-icon">📖</div><div class="feature-title">{{ i18n "menuTranslation" | default "Перевод" }}</div><p class="feature-desc">{{ i18n "featureTranslationDesc" | default "Полный текст Словесности." }}</p><span class="feature-arrow">{{ i18n "featureOpen" | default "Открыть" }} →</span></a>
                <a href="/{{ .Lang }}/articles/" class="feature-card"><div class="feature-icon">📑</div><div class="feature-title">{{ i18n "menuArticles" | default "Статьи" }}</div><p class="feature-desc">{{ i18n "featureArticlesDesc" | default "150+ материалов." }}</p><span class="feature-arrow">{{ i18n "featureView" | default "Смотреть" }} →</span></a>
                <a href="/{{ .Lang }}/monographs/" class="feature-card"><div class="feature-icon">📚</div><div class="feature-title">{{ i18n "menuMonographs" | default "Монографии" }}</div><p class="feature-desc">{{ i18n "featureMonographsDesc" | default "Научные монографии." }}</p><span class="feature-arrow">{{ i18n "featureOpen" | default "Открыть" }} →</span></a>
                <a href="/{{ .Lang }}/learning/" class="feature-card"><div class="feature-icon">🎓</div><div class="feature-title">{{ i18n "menuLearning" | default "Обучение" }}</div><p class="feature-desc">{{ i18n "featureLearningDesc" | default "Учебник арабского языка." }}</p><span class="feature-arrow">{{ i18n "featureStart" | default "Начать" }} →</span></a>
                <a href="/{{ .Lang }}/analytics/" class="feature-card"><div class="feature-icon">🔬</div><div class="feature-title">{{ i18n "menuAnalytics" | default "Аналитика" }}</div><p class="feature-desc">{{ i18n "featureAnalyticsDesc" | default "Исследования и аналитика." }}</p><span class="feature-arrow">{{ i18n "featureView" | default "Смотреть" }} →</span></a>
                <a href="/{{ .Lang }}/distribution/" class="feature-card"><div class="feature-icon">🌐</div><div class="feature-title">{{ i18n "menuDistribution" | default "Распространение" }}</div><p class="feature-desc">{{ i18n "featureDistributionDesc" | default "Каналы распространения." }}</p><span class="feature-arrow">{{ i18n "featureOpen" | default "Открыть" }} →</span></a>
            </div>
        </div>
    </section>

    <footer>
        <div class="footer-inner">
            <div class="footer-logo"><img src="/logo.png" alt="NQ"><span>NAR-UQ</span></div>
            <div class="footer-copy">© 2026 {{ .Site.Params.author }}</div>
            <div class="footer-contact"><a href="/{{ .Lang }}/contact/">{{ i18n "contact" | default "Связаться" }}</a></div>
        </div>
    </footer>
</body>
</html>
''')
print('index.html (partial) OK')

# ── 10. content/ru/monographs/index.md ───────────────────────────────────────
with open('content/ru/monographs/index.md', 'w') as f:
    f.write('---\ntitle: "Монографии"\n---\n\n')
    f.write('<div class="monographs-grid">\n')
    monos = [
        ('Формирование исламской нормативной системы в VII–XI вв.', 'Просопографический анализ интеллектуальной элиты', 'Арабы составляют лишь 19,6% кодификаторов. Просопографический анализ 97 суннитских и ~27 шиитских верифицированных фигур.', 'formirovanie islamskoy normativnoy sistemy.pdf'),
        ('Хадисоведение как институт предания', 'Эпистемические ограничения системы', 'Исследование эпистемических ограничений хадисоведения как системы верификации предания.', 'hadisovedeniye kak institut predaniya.pdf'),
        ('Текстологический статус Корана', 'Самореферентные указания как критерий идентификации аутентичного мусхафа', 'Методологически новый подход к датировке коранического текста.', 'tekstologicheskiy status korana.pdf'),
        ('Частица إِلَّا в Коране', 'Корпусный анализ 664 вхождений', 'Полный корпусный анализ всех вхождений частицы إِلَّا в Коране.', 'chastitsa illa v korane.pdf'),
        ('Прото-семитский корень ʔil', 'Лексикографическое исследование', 'Исследование прото-семитского корня ʔil и его производных в семитских языках.', 'proto semitskiy koren ill.pdf'),
        ('Онтология Ничто', 'Аксиоматическая система A1–A15', 'Философская монография. Аксиоматическая система A1–A15, лежащая в основе платформы Arbitrium.', 'ontologiya nichto.pdf'),
    ]
    for title, sub, desc, pdf in monos:
        f.write(f'<div class="mono-card"><div class="mono-icon">📖</div><div class="mono-title">{title}</div><div class="mono-subtitle">{sub}</div><p class="mono-desc">{desc}</p><a href="/{pdf}" class="mono-btn" download>Скачать PDF</a></div>\n')
    f.write('</div>\n')
print('monographs/index.md OK')

print('\nВсе файлы созданы.')
