import os, shutil, subprocess

# Убираем лишние папки
for bad in [
    'content/content',
    'layouts/layouts',
    'layouts/monographs',
]:
    if os.path.exists(bad):
        shutil.rmtree(bad)
        print(f'Removed: {bad}')

# Создаём correct single.html
os.makedirs('layouts/_default', exist_ok=True)
with open('layouts/_default/single.html', 'w') as f:
    f.write('{{ define "main" }}\n')
    f.write('<article style="padding: 140px 40px 80px; max-width: 1200px; margin: 0 auto;">\n')
    f.write('<h1 style="font-family: \'Playfair Display\',serif; font-size: 3rem; color: #1a6b6b;">{{ .Title }}</h1>\n')
    f.write('<div style="font-size: 1.1rem; line-height: 1.9;">{{ .Content }}</div>\n')
    f.write('</article>\n')
    f.write('{{ end }}\n')
print('single.html created')

# Проверяем content/ru/monographs/index.md
os.makedirs('content/ru/monographs', exist_ok=True)
if not os.path.exists('content/ru/monographs/index.md'):
    with open('content/ru/monographs/index.md', 'w') as f:
        f.write('---\ntitle: "Монографии"\n---\n\n')
        f.write('<div class="monographs-grid">\n')
        f.write('  <div class="mono-card"><div class="mono-icon">📖</div><div class="mono-title">Формирование исламской нормативной системы в VII–XI вв.</div><div class="mono-subtitle">Просопографический анализ интеллектуальной элиты</div><p class="mono-desc">Арабы составляют лишь 19,6% кодификаторов.</p><a href="/formirovanie islamskoy normativnoy sistemy.pdf" class="mono-btn" download>Скачать PDF</a></div>\n')
        f.write('  <div class="mono-card"><div class="mono-icon">📖</div><div class="mono-title">Хадисоведение как институт предания</div><div class="mono-subtitle">Эпистемические ограничения системы</div><p class="mono-desc">Исследование эпистемических ограничений хадисоведения.</p><a href="/hadisovedeniye kak institut predaniya.pdf" class="mono-btn" download>Скачать PDF</a></div>\n')
        f.write('  <div class="mono-card"><div class="mono-icon">📖</div><div class="mono-title">Текстологический статус Корана</div><div class="mono-subtitle">Самореферентные указания как критерий идентификации аутентичного мусхафа</div><p class="mono-desc">Методологически новый подход к датировке коранического текста.</p><a href="/tekstologicheskiy status korana.pdf" class="mono-btn" download>Скачать PDF</a></div>\n')
        f.write('  <div class="mono-card"><div class="mono-icon">📖</div><div class="mono-title">Частица إِلَّا в Коране</div><div class="mono-subtitle">Корпусный анализ 664 вхождений</div><p class="mono-desc">Полный корпусный анализ всех вхождений частицы إِلَّا в Коране.</p><a href="/chastitsa illa v korane.pdf" class="mono-btn" download>Скачать PDF</a></div>\n')
        f.write('  <div class="mono-card"><div class="mono-icon">📖</div><div class="mono-title">Прото-семитский корень ʔil</div><div class="mono-subtitle">Лексикографическое исследование</div><p class="mono-desc">Исследование прото-семитского корня ʔil и его производных.</p><a href="/proto semitskiy koren ill.pdf" class="mono-btn" download>Скачать PDF</a></div>\n')
        f.write('  <div class="mono-card"><div class="mono-icon">📖</div><div class="mono-title">Онтология Ничто</div><div class="mono-subtitle">Аксиоматическая система A1–A15</div><p class="mono-desc">Философская монография. Аксиоматическая система A1–A15.</p><a href="/ontologiya nichto.pdf" class="mono-btn" download>Скачать PDF</a></div>\n')
        f.write('</div>\n')
    print('index.md created')
else:
    print('index.md already exists')

print('Done')
