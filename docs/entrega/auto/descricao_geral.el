(TeX-add-style-hook
 "descricao_geral"
 (lambda ()
   (setq TeX-command-extra-options
         "-shell-escape")
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt" "a4paper")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("ulem" "normalem") ("geometry" "left=3cm" "top=3cm" "right=2cm" "bottom=2cm") ("babel" "brazilian" "")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art11"
    "inputenc"
    "fontenc"
    "graphicx"
    "grffile"
    "longtable"
    "wrapfig"
    "rotating"
    "ulem"
    "amsmath"
    "textcomp"
    "amssymb"
    "capt-of"
    "hyperref"
    "geometry"
    "babel"
    "indentfirst")
   (LaTeX-add-labels
    "sec:org42fe0eb"
    "sec:org4c57f53"
    "sec:org7a53bc8"
    "sec:orgbb00d6a"
    "sec:org98c08c4"
    "sec:orgd29618a"
    "sec:orgbc16847"
    "sec:org1aa3510"
    "sec:org7296298"
    "org376bcb0"
    "sec:orgb6bc9f4"
    "orge0df9e4"
    "sec:org4375ff5"
    "org2d92571"
    "sec:org1d2e3c9"))
 :latex)

