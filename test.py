import re
text = """song – damru ala
singer – billa sonipat ala
lyrics – billa sonipat ala
music – deepty
label – white hill dhaakad"""
print(text.replace("\n","<BR>"))
data = re.findall(r"(?<=–).*?(?=<BR>)", text.replace("\n","<BR>"))
print(data)