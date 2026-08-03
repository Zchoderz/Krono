import os
import glob

html_files = glob.glob('*.html')

head_injection = """  <link rel="stylesheet" href="transitions.css">
  <script src="transitions.js" defer></script>
</head>"""

body_injection = """<body>
  <div id="page-transition-loader">
    <div class="loader-spinner"></div>
  </div>
  <button id="back-to-top" aria-label="Back to top">↑</button>"""

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'transitions.css' not in content:
        content = content.replace('</head>', head_injection)
        content = content.replace('<body>', body_injection)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Injected into {file}")
    else:
        print(f"Already injected in {file}")
