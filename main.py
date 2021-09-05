from htmlGen import magx_HTML
from htmlString import ht
if __name__ == '__main__':
    html = magx_HTML(ht)
    out = html.getHTML()
    print(out)

