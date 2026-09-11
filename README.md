# 🤖 Amigo - Discord Bot

Um bot Discord que funciona como um "amigo" resposnador, permitindo reenviar mensagens através de webhooks com avatar e nome personalizados.

## 📋 Requisitos

- Python 3.8+
- Discord.py
- Token de bot Discord

## 🚀 Como Usar

### 1. Configurar no Replit

1. Vá para **Secrets** (ícone de chave 🔑) no painel esquerdo
2. Adicione as seguintes variáveis de ambiente:

| Variável | Descrição | Obrigatório |
|----------|-----------|------------|
| `DISCORD_TOKEN` | Token do seu bot Discord | ✅ Sim |
| `GIF_URL` | URL de um GIF para anexar às mensagens | ❌ Opcional |
| `NORMAL_MARKER` | Marcador para mensagens normais (padrão: `-testar-`) | ❌ Opcional |
| `WEBHOOK_MARKER` | Marcador para mensagens de webhook (padrão: `-testarw-`) | ❌ Opcional |

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o bot

```bash
python main.py
```

## 🎯 Como Funciona

1. **Mensagens Normais**: Envie uma mensagem contendo `-testar-` (ex: `-testar- Olá!`)
2. **Mensagens de Webhook**: Envie via webhook contendo `-testarw-` (ex: `-testarw- Olá!`)
3. O bot irá:
   - Deletar a mensagem original
   - Criar/usar um webhook chamado "Reenvio"
   - Reenviar a mensagem com seu nome e avatar
   - Adicionar um GIF (se configurado)

## 📝 Exemplo de Uso

```
Você: -testar- Oi galera!

Bot: [Reenvia como você via webhook]
     Oi galera!
     https://tenor.com/view/... (GIF)
```

## ⚙️ Configuração do Bot Discord

1. Vá para [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação
3. Na aba **Bot**, clique em **Add Bot**
4. Copie o **TOKEN** e adicione em Secrets do Replit como `DISCORD_TOKEN`
5. Ative as **Intents**:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
6. Gere uma URL de convite com as permissões:
   - Manage Webhooks
   - Send Messages
   - Delete Messages
   - Read Message History

## 🐛 Troubleshooting

- **Bot não conecta**: Verifique se `DISCORD_TOKEN` está configurado corretamente nos Secrets
- **Sem permissão para apagar mensagens**: O bot precisa de permissão "Manage Messages" no canal
- **Webhook não é criado**: Verifique se o bot tem permissão "Manage Webhooks"

## 📦 Dependências

- `discord.py` - Biblioteca oficial para bots Discord

## 📄 Licença

MIT

---

**Desenvolvido com ❤️**
