from flask import Flask, render_template, redirect, url_for, request
from mysql import connector
app = Flask(__name__)

db = connector.connect(
	host	= "localhost",
	user	= "root",
	passwd	= "",
	database= "rental_kamera"
)

@app.route('/')
def halaman_utama():
	return render_template('h_utama.html')

@app.route('/sewa')
def sewa():
	return render_template('h_sewa.html')

@app.route('/sewa',methods=['GET','POST'])
def proses_sewa():
	global total, kamera, idpenyewa, test1, kamera1
	nama = request.form['nama']
	no_tlp = request.form['nomer']
	id_card = request.form['card']

	cur = db.cursor()
	cur.execute('INSERT INTO penyewa(nama,no_telp,id_card) VALUES (%s,%s,%s)',(nama, no_tlp, id_card))
	db.commit()

	proses_sewa.kamera = request.form['kamera']
	durasi = request.form['durasi']

	durasi1 = int(durasi)

	if proses_sewa.kamera == 'C1':
		total = durasi1 * 80000
	if proses_sewa.kamera == 'C2':
		total = durasi1 * 100000
	if proses_sewa.kamera == 'N1':
		total = durasi1 * 120000
	if proses_sewa.kamera == 'N2':
		total = durasi1 * 150000
	if proses_sewa.kamera == 'S1':
		total = durasi1 * 200000
	if proses_sewa.kamera == 'S2':
		total = durasi1 * 250000

	cur2 = db.cursor()
	cur2.execute('SELECT id_penyewa FROM penyewa')
	for row in cur2:
		idpenyewa = (max(row))


	cur4 = db.cursor()
	cur4.execute('INSERT INTO sewa(id_penyewa, id_kamera, durasi, total) VALUES (%s, %s, %s, %s)',
				 (idpenyewa, proses_sewa.kamera, durasi, total))
	db.commit()
	return redirect(url_for('hasil_sewa'))


@app.route('/rental/Hasil')
def hasil_sewa():
	cur = db.cursor()
	cur.execute("select sewa.id_sewa, penyewa.nama, card.keterangan, kamera.merek, sewa.durasi, sewa.total FROM sewa, penyewa, card, kamera WHERE sewa.id_penyewa= penyewa.id_penyewa AND sewa.id_kamera = kamera.id_kamera AND card.id_card=penyewa.id_card order by sewa.id_sewa desc limit 1 ")
	res = cur.fetchall()

	return render_template('h_hasil.html', hasil=res)


if db.is_connected():
	print("Berhasil Terhubung ke Database")

if __name__ == '__main__':
	app.run()