# RetinaPY

GUI amigável para predição de eventos adversos envolvendo análise de imagem de Tomografia de Coerência Óptica (OCT). \
Utiliza o modelo pré-treinado [Kermany](https://www.sciencedirect.com/science/article/pii/S0092867418301545), o qual dispõe de milhares de imagens de OCTs para treinamento da IA.


## Como usar:

Baixar o modelo já treinado pelo link: [Download](https://drive.google.com/file/d/1OGGOJtx-nzUfo4DZMC6yGf7e3zvKzAIg/view?usp=sharing) \
OBS: **o modelo precisa estar no mesmo diretório raiz da aplicação!** \
Rodar, no diretório raiz, ```pip install -r requirements.txt``` \
A aplicação que deve ser executada é a ```gui.pyw``` (Caso não seja Windos, executar a ```gui.py```)

## Descrição

 A IA foi treinada para gerar 4 tipos de outputs:
 

 - Diabetic Macular Edema (DME);
 - Choroidal Neovascularization (CNV);
 - Drusen;
 - Normal.
 
 
**Informações do modelo:**  288 camadas; 11.972.940 número total de weights; eficácia de 99,8%

## Prints do programa:
- **Geral:** \
![Print de tela do programa em funcionamento](https://i.imgur.com/NT2Hktl.png) \

- **Log:** \
![Print de tela do histórico de outputs do programa](https://i.imgur.com/cVWQrok.png)


## Log em .csv

O programa salva em .csv os outputs em ordem cronológica. Contém a probabilidade de cada condição para cada foto selecionada.

## Créditos
Idealizado por [Thiago Narcizo](https://github.com/thiagonarcizo/) e [Matheus Arthur](https://github.com/mathfaria)
> -   S. A. Kamran, S. Saha, A. S. Sabbir, A. Tavakkoli, "Optic-Net: A Novel Convolutional Neural Network for Diagnosis of Retinal Diseases from Optical Tomography Images," DOI: 10.1109/ICMLA.2019.00165 (2019)
> - Disponível em: [https://github.com/SharifAmit/OpticNet-71](https://github.com/SharifAmit/OpticNet-71)
