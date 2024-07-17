from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta, date
import os


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = os.urandom(24)


app.config['S   QLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/luxury.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    reservas = db.relationship('Reserva', backref='cliente', lazy=True)


class Veiculo(db.Model):
    __tablename__ = 'veiculos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    img_src = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    transmissao = db.Column(db.String(50), nullable=False)
    valor_diaria = db.Column(db.Integer, nullable=False)
    nr_passageiros = db.Column(db.Integer, nullable=False)
    ultima_inspecao = db.Column(db.Date, nullable=True)
    proxima_inspecao = db.Column(db.Date, nullable=True)
    disponivel = db.Column(db.Boolean, default=True)

    reservas = db.relationship('Reserva', backref='veiculo', lazy=True)

    def __repr__(self):
        return (f"Veiculo(nome={self.nome}, tipo={self.tipo}, categoria={self.categoria},"
                f" transmissao={self.transmissao}, valor_diaria={self.valor_diaria},"
                f" nr_passageiros={self.nr_passageiros}, ultima_inspecao={self.ultima_inspecao},"
                f" proxima_inspecao={self.proxima_inspecao}, disponivel={self.disponivel})")


class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculos.id'), nullable=False)
    total_reserva = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return (f"Reserva(cliente_id={self.cliente_id},"
                f" veiculo_id={self.veiculo_id}, total_reserva={self.total_reserva},"
                f" start_date={self.start_date}, end_date={self.end_date})")

    pagamento = db.relationship('Pagamento', backref='reserva', uselist=False, lazy=True)


class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    id = db.Column(db.Integer, primary_key=True)
    reserva_id = db.Column(db.Integer, db.ForeignKey('reservas.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()

    veiculos = [
        {
            "nome": "Peugeot 208",
            "img_src": "/static/peugeot_208.jpeg",
            "tipo": "carro",
            "categoria": "medio",
            "transmissao": "manual",
            "valor_diaria": 55,
            "nr_passageiros": 5,
            "ultima_inspecao": datetime(2023, 3, 15),
            "proxima_inspecao": datetime(2024, 3, 15),
        },
        {
            "nome": "Mini Cooper S",
            "img_src": "/static/mini_cooper_s.jpeg",
            "tipo": "carro",
            "categoria": "medio",
            "transmissao": "manual",
            "valor_diaria": 60,
            "nr_passageiros": 4,
            "ultima_inspecao": datetime(2023, 2, 20),
            "proxima_inspecao": datetime(2024, 2, 20),
        },
        {
            "nome": "Golf GTI",
            "img_src": "/static/golf_gti.jpeg",
            "tipo": "carro",
            "categoria": "medio",
            "transmissao": "manual",
            "valor_diaria": 70,
            "nr_passageiros": 5,
            "ultima_inspecao": datetime(2023, 7, 24),
            "proxima_inspecao": datetime(2024, 7, 24),
        },
        {
            "nome": "Ford Puma",
            "img_src": "/static/ford_puma.jpeg",
            "tipo": "carro",
            "categoria": "suv",
            "transmissao": "manual",
            "valor_diaria": 70,
            "nr_passageiros": 5,
            "ultima_inspecao": datetime(2023, 8, 14),
            "proxima_inspecao": datetime(2024, 8, 14),
        },
        {
            "nome": "Citroen E-Spacetourer",
            "img_src": "/static/citroen_e-spacetourer.jpeg",
            "tipo": "carro",
            "categoria": "grande",
            "transmissao": "manual",
            "valor_diaria": 90,
            "nr_passageiros": 9,
            "ultima_inspecao": datetime(2023, 10, 4),
            "proxima_inspecao": datetime(2024, 10, 4),
        },
        {
            "nome": "Tesla Roadster",
            "img_src": "/static/tesla_roadster.jpeg",
            "tipo": "carro",
            "categoria": "medio",
            "transmissao": "automatica",
            "valor_diaria": 300,
            "nr_passageiros": 4,
            "ultima_inspecao": datetime(2023, 12, 28),
            "proxima_inspecao": datetime(2024, 12, 28),
        },
        {
            "nome": "CBR 600",
            "img_src": "/static/cbr_600.jpeg",
            "tipo": "moto",
            "categoria": "pequeno",
            "transmissao": "automatica",
            "valor_diaria": 50,
            "nr_passageiros": 2,
            "ultima_inspecao": datetime(2023, 11, 28),
            "proxima_inspecao": datetime(2024, 11, 28),
        },
        {
            "nome": "Kawasaki Ninja",
            "img_src": "/static/kawasaki_ninja.jpeg",
            "tipo": "moto",
            "categoria": "pequeno",
            "transmissao": "automatica",
            "valor_diaria": 60,
            "nr_passageiros": 2,
            "ultima_inspecao": datetime(2023, 9, 21),
            "proxima_inspecao": datetime(2024, 9, 21),
        },

    ]

    for veiculo_data in veiculos:
        veiculo_existente = Veiculo.query.filter_by(nome=veiculo_data["nome"]).first()
        if veiculo_existente:
            print(f"O veículo {veiculo_data['nome']} já existe, sendo assim não foi adicionado à base de dados.")
            continue

        novo_veiculo = Veiculo(
            nome=veiculo_data["nome"],
            img_src=veiculo_data["img_src"],
            tipo=veiculo_data["tipo"],
            categoria=veiculo_data["categoria"],
            transmissao=veiculo_data["transmissao"],
            valor_diaria=veiculo_data["valor_diaria"],
            nr_passageiros=veiculo_data["nr_passageiros"],
            ultima_inspecao=veiculo_data["ultima_inspecao"],
            proxima_inspecao=veiculo_data["proxima_inspecao"]
        )
        print(f"Adicionando veículo: {novo_veiculo.nome}")
        try:
            db.session.add(novo_veiculo)
            db.session.commit()
            print(f"Veículo {novo_veiculo.nome} adicionado com sucesso!")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao adicionar veículo {novo_veiculo.nome}: {str(e)}")


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cliente = Cliente.query.filter_by(username=username).first()

        if cliente and bcrypt.check_password_hash(cliente.password, password):
            session['user_id'] = cliente.id
            session['user_email'] = cliente.email
            return redirect(url_for('catalog'))
        else:
            return render_template("index.html", error="Username ou password incorretos.")

    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template("register.html", error="As passwords nao coincidem.")

        hashed_password = bcrypt.generate_password_hash(password)

        new_cliente = Cliente(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_cliente)
            db.session.commit()
            print("Usuário registrado com sucesso!")
            return render_template("register.html", message="O seu registo foi efetuado com sucesso!")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao registrar usuário: {str(e)}")
            return render_template("register.html", error="Ocorreu um erro ao tentar registrar o usuário.")

    return render_template("register.html")


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    hoje = date.today()

    if request.method == 'POST':
        filtro_tipo = request.form.get('tipo')
        filtro_categoria = request.form.get('categoria')
        filtro_transmissao = request.form.get('transmissao')
        filtro_valor_diaria = request.form.get('diaria')
        filtro_nr_passageiros = request.form.get('nr_passageiros')

        print(
            f"Filtros recebidos: tipo={filtro_tipo}, categoria={filtro_categoria}, transmissao={filtro_transmissao}"
            f", diaria={filtro_valor_diaria}, nr_passageiros={filtro_nr_passageiros}")

        query = Veiculo.query.filter(Veiculo.proxima_inspecao > hoje, Veiculo.disponivel == True)

        if filtro_tipo != 'todos' and filtro_tipo:
            query = query.filter_by(tipo=filtro_tipo)
        if filtro_categoria != 'todos' and filtro_categoria:
            query = query.filter_by(categoria=filtro_categoria)
        if filtro_transmissao != 'todos' and filtro_transmissao:
            query = query.filter_by(transmissao=filtro_transmissao)
        if filtro_valor_diaria != 'todos' and filtro_valor_diaria:
            if filtro_valor_diaria == '<25':
                query = query.filter(Veiculo.valor_diaria < 25)
            elif filtro_valor_diaria == '25-50':
                query = query.filter(Veiculo.valor_diaria.between(25, 50))
            elif filtro_valor_diaria == '50-75':
                query = query.filter(Veiculo.valor_diaria.between(50, 75))
            elif filtro_valor_diaria == '75-100':
                query = query.filter(Veiculo.valor_diaria.between(75, 100))
            elif filtro_valor_diaria == '>100':
                query = query.filter(Veiculo.valor_diaria > 100)
        if filtro_nr_passageiros != 'todos' and filtro_nr_passageiros:
            if filtro_nr_passageiros == '1-4':
                query = query.filter(Veiculo.nr_passageiros.between(1, 4))
            elif filtro_nr_passageiros == '5-6':
                query = query.filter(Veiculo.nr_passageiros.between(5, 6))
            elif filtro_nr_passageiros == '>7':
                query = query.filter(Veiculo.nr_passageiros > 6)

        veiculos_filtrados = query.all()
        print(f"Número de veículos filtrados: {len(veiculos_filtrados)}")

        return render_template("catalog.html", veiculos=veiculos_filtrados)

    else:
        veiculos = Veiculo.query.filter(Veiculo.proxima_inspecao > hoje, Veiculo.disponivel == True).all()
        return render_template("catalog.html", veiculos=veiculos)


@app.route('/booking/<int:veiculo_id>', methods=['GET', 'POST'])
def booking(veiculo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    veiculo = Veiculo.query.get_or_404(veiculo_id)
    error_message = ""

    hoje = datetime.today().strftime('%Y-%m-%d')
    amanha = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    start_date = request.form.get('start_date', hoje)
    end_date = request.form.get('end_date', amanha)

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        if end_date <= start_date:
            error_message = "A data de término deve ser superior à data de início."
        else:
            total_reserva = calcular_total_reserva(start_date, end_date, veiculo.valor_diaria)
            cliente_id = session['user_id']
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            nova_reserva = Reserva(
                cliente_id=cliente_id,
                veiculo_id=veiculo.id,
                total_reserva=total_reserva,
                start_date=start_date,
                end_date=end_date
            )
            db.session.add(nova_reserva)
            db.session.commit()

            if 'reserva' in request.form:
                return redirect(url_for('payment'))
            return render_template('booking.html', veiculo=veiculo, total_reserva=total_reserva, start_date=start_date, end_date=end_date, hoje=hoje, amanha=amanha, error_message=error_message)

    return render_template('booking.html', veiculo=veiculo, hoje=hoje, amanha=amanha, start_date=start_date, end_date=end_date, error_message=error_message)

def calcular_total_reserva(start_date, end_date, valor_diaria):
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        delta = (end_date - start_date).days + 1
        total = delta * valor_diaria
        return total
    except ValueError:
        return None


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        metodo_pagamento = request.form['metodo_pagamento']
        return render_template('payment.html', metodo_pagamento=metodo_pagamento)

    return render_template('payment.html')


@app.route('/process_payment', methods=['POST'])
def process_payment():
    metodo_pagamento = request.form.get('metodo_pagamento')

    cliente_id = session['user_id']
    ultima_reserva = Reserva.query.filter_by(cliente_id=cliente_id).order_by(Reserva.id.desc()).first()

    if not ultima_reserva:
        flash('Você não possui nenhuma reserva para efetuar um pagamento.', 'error')
        return redirect(url_for('catalog'))

    novo_pagamento = Pagamento(
        cliente_id=cliente_id,
        reserva_id=ultima_reserva.id,
        forma_pagamento=metodo_pagamento
    )

    try:
        db.session.add(novo_pagamento)
        veiculo = Veiculo.query.get(ultima_reserva.veiculo_id)
        veiculo.disponivel = False
        db.session.commit()
        flash('Pagamento efetuado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao processar pagamento: {str(e)}', 'error')

    return redirect(url_for('catalog'))

@app.route('/historic', methods=['GET', 'POST'])
def historic():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cliente_id = session['user_id']
    reservas = Reserva.query.filter_by(cliente_id=cliente_id).all()
    return render_template('historic.html', reservas=reservas)

@app.route('/edit_reserva/<int:reserva_id>', methods=['POST'])
def edit_reserva(reserva_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    reserva = Reserva.query.get_or_404(reserva_id)

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        reserva.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        reserva.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        reserva.total_reserva = calcular_total_reserva(start_date, end_date, reserva.veiculo.valor_diaria)

        try:
            db.session.commit()
            flash('Reserva atualizada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar reserva: {str(e)}', 'error')

        return redirect(url_for('historic'))

    return render_template('edit_reserva.html', reserva=reserva)

@app.route('/cancel_reserva/<int:reserva_id>', methods=['POST'])
def cancel_reserva(reserva_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    reserva = Reserva.query.get_or_404(reserva_id)

    try:
        pagamento = Pagamento.query.filter_by(reserva_id=reserva.id).first()
        if pagamento:
            db.session.delete(pagamento)

        veiculo = Veiculo.query.get(reserva.veiculo_id)
        veiculo.disponivel = True

        db.session.delete(reserva)

        db.session.commit()

        flash('Reserva cancelada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cancelar reserva: {str(e)}', 'error')

    return redirect(url_for('historic'))

if __name__ == '__main__':
    app.run()
