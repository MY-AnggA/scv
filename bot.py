from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import paramiko

# Fungsi untuk menangani perintah /start
def start(update, context):
    update.message.reply_text("Halo! Silakan kirimkan nama, tahun, bulan, dan tanggal.")

# Fungsi untuk menangani pesan input
def input_handler(update, context):
    text = update.message.text
    chat_id = update.message.chat_id

    try:
        # Membagi input menjadi nama, tahun, bulan, dan tanggal
        nama, tahun, bulan, tanggal = text.split()
        
        # Simpan input ke file ip.txt di hosting menggunakan SSH
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect('hosting_ip_address', username='username', password='password')
        sftp_client = ssh_client.open_sftp()
        with sftp_client.file('/path/to/ip.txt', 'a') as file:
            file.write(f'{nama}, {tahun}, {bulan}, {tanggal}\n')
        sftp_client.close()
        ssh_client.close()
        
        update.message.reply_text("Input berhasil disimpan.")
    except Exception as e:
        update.message.reply_text("Terjadi kesalahan dalam pemrosesan input.")

# Fungsi utama
def main():
    # Inisialisasi updater dan dispatcher
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    
    # Menambahkan handler untuk perintah /start
    dp.add_handler(CommandHandler("start", start))
    
    # Menambahkan handler untuk pesan input
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, input_handler))
    
    # Memulai bot
    updater.start_polling()
    
    # Bot akan berjalan sampai proses dihentikan
    updater.idle()

if __name__ == '__main__':
    main()