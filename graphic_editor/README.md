# Grafický editor

**Grafický editor** je jednoduchá CLI aplikace, která dokáže načíst vstupní obrázek, na něm provádět vybrané základní grafické operace a výstup uložit. Mezi operace, které tato aplikace nabízí, patří:

* rozostření,
* převod do odstínů šedi,
* ztmavení,
* detekce hran,
* reliéf,
* inverze,
* zesvětlení,
* zrcadlení,
* rotace o 90° vpravo,
* doostření.

# Ovládání

Aplikace se ovládá pomocí následujícího příkazu:

_python graphic_editor [filtry] [cesta ke vstupnímu obrázku] [cesta k výstupnímu obrázku]_

Jednotlivé filtry je možné mezi sebou libovolně kombinovat.

# Filtry

### Rozostření

**Příkaz:** _--blur_

![blur](/graphic_editor/tests/blur.png)

### Převod do odstínů šedi

**Příkaz:** _--bw_

![bw](/graphic_editor/tests/bw.png)

### Ztmavení

**Příkaz:** _--darken [0–100]_

![darken](/graphic_editor/tests/darken.png)

### Detekce hran

**Příkaz:** _--edges_

![edges](/graphic_editor/tests/edges.png)

### Reliéf

**Příkaz:** _--emboss_

![emboss](/graphic_editor/tests/emboss.png)

### Inverze

**Příkaz:** _--inverse_

![inverse](/graphic_editor/tests/inverse.png)

### Zesvětlení

**Příkaz:** _--lighten [0–100]_

![lighten](/graphic_editor/tests/lighten.png)

### Zrcadlení

**Příkaz:** _--mirror_

![mirror](/graphic_editor/tests/mirror.png)

### Rotace o 90° vpravo

**Příkaz:** _--rotate_

![rotate](/graphic_editor/tests/rotate.png)

### Doostření (pomocí konvoluce)

**Příkaz:** _--sharpen_

![sharpen](/graphic_editor/tests/sharpen.png)

### Doostření (pomocí techniky USM)

**Příkaz:** _--unsharpmask [0–100]_

![unsharpmask](/graphic_editor/tests/unsharpmask.png)