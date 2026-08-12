# 🤖 Bot de Discord Multifuncional

Um bot para Discord desenvolvido em Python utilizando `discord.py`. Ele conta com um sistema de música integrado ao YouTube via `yt-dlp` e consultas climáticas em tempo real.

---

## 🚀 Comandos Disponíveis

O bot utiliza **Slash Commands** (`/`), facilitando a interação e autocompletando as opções diretamente no Discord.

| Comando | Parâmetros | Descrição |
| :--- | :--- | :--- |
| `/ping` | Nenhum | Testa se o bot está online e responsivo. |
| `/clima` | `cidade` (Obrigatório) | Retorna as condições climáticas atuais da cidade informada. |
| `/play` | `busca` (Obrigatório) | Conecta ao canal de voz e toca uma música do YouTube (aceita URL ou nome da música). |
| `/stop` | Nenhum | Interrompe a reprodução da música atual. |
| `/leave` | Nenhum | Desconecta o bot do canal de voz. |

---

## ⚙️ Pré-requisitos

Para rodar este bot na sua máquina, você precisará das seguintes ferramentas:

* **Python 3.8+** instalado.
* **FFmpeg**: O arquivo `ffmpeg.exe` precisa estar na mesma pasta raiz do projeto, pois o código faz referência direta a ele (`executable="./ffmpeg.exe"`).
* Conta no [Discord Developer Portal](https://discord.com/developers/applications) para obter o Token do bot.

---

## 🛠️ Como Instalar e Configurar

Siga o passo a passo abaixo para rodar o projeto localmente:

1. **Faça o download ou clone este repositório** para o seu computador.
2. **Abra o terminal** na pasta do projeto.
3. **Instale as bibliotecas necessárias** rodando o seguinte comando:
   ```bash
   pip install discord.py python-dotenv aiohttp yt-dlp pynacl