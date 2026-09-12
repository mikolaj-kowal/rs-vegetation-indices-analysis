# Analiza porównawcza wskaźników roślinności z wykorzystaniem danych Sentinel-2

_Zastrzeżenie: Projekt edukacyjny mający na celu praktyczne zastosowanie wiedzy zdobytej w zakresie teledetekcji satelitarnej oraz podstaw przetwarzania i analizy danych przestrzennych._

Wskaźniki roślinności (ang. vegetation indices) to wskaźniki teledetekcyjne obliczane na podstawie odbicia promieniowania w wybranych pasmach spektralnych, służące do oceny stanu i kondycji roślinności.

W tym projekcie porównuję różne wskaźniki roślinności obliczone na podstawie tego samego zobrazowania satelitarnego Sentinel-2. Analizuję, w jaki sposób poszczególne wskaźniki charakteryzują roślinność oraz jak różnią się uzyskane rozkłady wartości.

<details>
<summary><strong>Informacje o projekcie</strong></summary>

##### Wykorzystane narzędzia

- [Python](https://www.python.org/)
- [JupyterLab](https://jupyter.org/)

</details>

<br>
<div align="center">
<em>Tabela 1. Charakterystyka pasm spektralnych satelitów Sentinel-2</em>
<table border="1">
  <thead>
    <tr style="text-align: left;">
      <th></th>
      <th>Sentinel-2A</th>
      <th></th>
      <th>Sentinel-2B</th>
    </tr>
    <tr style="text-align: left;">
      <th>Band Number</th>
      <th>Central wavelength (nm)</th>
      <th>Bandwidth (nm)</th>
      <th>Central wavelength (nm)</th>
      <th>Bandwidth (nm)</th>
      <th>Spatial resolution (m)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>442.7</td>
      <td>20</td>
      <td>442.3</td>
      <td>20</td>
      <td>60</td>
    </tr>
    <tr>
      <td>2</td>
      <td>492.7</td>
      <td>65</td>
      <td>492.3</td>
      <td>65</td>
      <td>10</td>
    </tr>
    <tr>
      <td>3</td>
      <td>559.8</td>
      <td>35</td>
      <td>558.9</td>
      <td>35</td>
      <td>10</td>
    </tr>
    <tr>
      <td>4</td>
      <td>664.6</td>
      <td>30</td>
      <td>664.9</td>
      <td>31</td>
      <td>10</td>
    </tr>
    <tr>
      <td>5</td>
      <td>704.1</td>
      <td>14</td>
      <td>703.8</td>
      <td>15</td>
      <td>20</td>
    </tr>
    <tr>
      <td>6</td>
      <td>740.5</td>
      <td>14</td>
      <td>739.1</td>
      <td>13</td>
      <td>20</td>
    </tr>
    <tr>
      <td>7</td>
      <td>782.8</td>
      <td>19</td>
      <td>779.7</td>
      <td>19</td>
      <td>20</td>
    </tr>
    <tr>
      <td>8</td>
      <td>832.8</td>
      <td>105</td>
      <td>832.9</td>
      <td>104</td>
      <td>10</td>
    </tr>
    <tr>
      <td>8a</td>
      <td>864.7</td>
      <td>21</td>
      <td>864.0</td>
      <td>21</td>
      <td>20</td>
    </tr>
    <tr>
      <td>9</td>
      <td>945.1</td>
      <td>19</td>
      <td>943.2</td>
      <td>20</td>
      <td>60</td>
    </tr>
    <tr>
      <td>10</td>
      <td>1373.5</td>
      <td>29</td>
      <td>1376.9</td>
      <td>29</td>
      <td>60</td>
    </tr>
    <tr>
      <td>11</td>
      <td>1613.7</td>
      <td>90</td>
      <td>1610.4</td>
      <td>94</td>
      <td>20</td>
    </tr>
    <tr>
      <td>12</td>
      <td>2202.4</td>
      <td>174</td>
      <td>2185.7</td>
      <td>184</td>
      <td>20</td>
    </tr>
  </tbody>
</table>
<em style="font-size: 0.85em;">Źródło: https://www.earthdata.nasa.gov/data/instruments/sentinel-2-msi</em>
</div>

