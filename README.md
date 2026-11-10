# 3DME — Idol Studio

Aplicativo local em português para transformar uma imagem em um modelo 3D Gaussian Splat e exportar em PLY.

## Requisitos

- Windows 10 64 bits
- Python 3.11 x64
- Git for Windows
- GPU NVIDIA com driver atualizado
- Internet para instalação e download inicial dos modelos

A RTX 3060 é compatível com CUDA. A memória varia entre versões de 8 GB e 12 GB. Comece com 65.536 ou 131.072 Gaussians. O projeto original documenta pico de até cerca de 7,2 GB de VRAM, portanto 8 GB pode ficar no limite. Não há benchmark específico para cada variante da RTX 3060.

## Instalação

1. Instale Python 3.11 x64: https://www.python.org/downloads/
2. Marque Add Python to PATH.
3. Instale Git for Windows: https://git-scm.com/download/win
4. Atualize o driver NVIDIA.
5. Clone este repositório usando: git clone -b idol-studio https://github.com/ressignifiquesp-svg/3dme.git
6. Abra a pasta 3dme e execute instalar.bat.
7. Aguarde a instalação do PyTorch CUDA e do Idol SDK.

## Acesso aos modelos Hugging Face

O SDK original exige solicitar acesso e aceitar os termos destes modelos:

- https://huggingface.co/facebook/dinov3-vith16plus-pretrain-lvd1689m
- https://huggingface.co/black-forest-labs/FLUX.2-dev

Depois, abra o Prompt de Comando na pasta do projeto e execute:

    .venv\Scripts\activate
    hf auth login

Informe seu token Hugging Face quando solicitado. Não coloque tokens em arquivos do projeto nem os compartilhe.

## Abrir o aplicativo

Execute iniciar.bat. A interface abrirá em:

http://127.0.0.1:7860

A aplicação escuta somente em 127.0.0.1 e não cria link público.

## Uso

1. Envie uma imagem JPG, PNG ou WEBP.
2. Escolha Imagem/render 3D para imagens geradas por computador ou Fotografia real para fotos.
3. Escolha a quantidade de Gaussians. Comece em 65.536 para testar.
4. Clique em GERAR MODELO 3D.
5. Baixe o arquivo PLY.

Os resultados ficam em outputs. O histórico mostra os 30 arquivos mais recentes.

## Solução de problemas

- CUDA não detectada: atualize o driver NVIDIA e confirme o PyTorch CUDA no ambiente .venv.
- Falta de VRAM: reduza a quantidade de Gaussians e feche programas que usam a GPU.
- Acesso negado ao modelo: confirme que aceitou os termos dos dois repositórios Hugging Face e executou hf auth login.
- Falha de dependências: verifique internet e espaço em disco e execute instalar.bat novamente.

## SDK original

O instalador baixa o SDK oficial em vendor/idol-sdk, sem copiar ou modificar seu código-fonte. Projeto original: https://github.com/speridlabs/idol-sdk

Consulte o README e a licença Apache-2.0 do SDK antes de redistribuir ou modificar o projeto.
