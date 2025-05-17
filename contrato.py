import streamlit as st
from fpdf import FPDF
from datetime import datetime, date

def format_currency(value):
    value = ''.join(filter(lambda x: x.isdigit() or x == ',', value))
    value = value.replace(',', '.')
    try:
        fvalue = float(value)
        return f"R$ {fvalue:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return value

st.title("Gerador de Contrato de Locação")

nome = st.text_input("Nome do Locatário")
cpf = st.text_input("CPF do Locatário")
telefone = st.text_input("Telefone do Locatário")
endereco = st.text_input("Endereço do Imóvel a ser alugado")

# 👇 Alteração feita aqui para permitir anos mais antigos:
data_nascimento = st.date_input(
    "Data de Nascimento do Locatário",
    value=date(1990, 1, 1),
    min_value=date(1900, 1, 1),
    max_value=date.today()
)

st.write("Data selecionada:", data_nascimento.strftime("%d/%m/%Y"))
nome_mae = st.text_input("Nome da Mãe do Locatário")

locador_nome = "Laercio Donizete Pedroso"
locador_cpf = "11111111111"
locador_data_nasc = datetime.strptime("20/12/1967", "%d/%m/%Y").date()

valor_aluguel_input = st.text_input("Valor do Aluguel (R$)")
valor_aluguel = valor_aluguel_input

if valor_aluguel_input:
    valor_aluguel = format_currency(valor_aluguel_input)
    st.write(f"Valor formatado: {valor_aluguel}")

if st.button("Gerar Contrato"):
    if not (nome and cpf and telefone and endereco and nome_mae and valor_aluguel_input):
        st.error("Por favor, preencha todos os campos.")
    else:
        data_nasc_locatario = data_nascimento.strftime("%d/%m/%Y")
        data_nasc_locador = locador_data_nasc.strftime("%d/%m/%Y")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)

        pdf.cell(0, 8, "Contrato de Locação", ln=True, align="C")
        pdf.ln(5)

        locador_texto = (
            f"LOCADOR: {locador_nome}, CPF: {locador_cpf}, Data de Nascimento: {data_nasc_locador}."
        )
        pdf.multi_cell(0, 10, locador_texto)
        pdf.ln(3)

        locatario_texto = (
            f"LOCATÁRIO: {nome}, CPF: {cpf}, Telefone: {telefone}, Endereço do Imóvel: {endereco}, "
            f"Data de Nascimento: {data_nasc_locatario}, Nome da Mãe: {nome_mae}."
        )
        pdf.multi_cell(0, 6, locatario_texto)
        pdf.ln(3)

        pdf.multi_cell(0, 6, f"Valor do Aluguel: {valor_aluguel} (reais)")
        pdf.ln(5)

        clausulas = [
            "1. O LOCADOR é o legítimo proprietário do imóvel objeto deste contrato.",
            "2. O LOCATÁRIO declara conhecer as condições do imóvel e aceita alugá-lo pelo prazo estabelecido.",
            "3. O valor do aluguel mensal será pago até o dia 5 (cinco) de cada mês, mediante depósito na conta indicada pelo LOCADOR.",
            "4. O LOCATÁRIO se compromete a zelar pelo imóvel, responsabilizando-se por danos causados durante a vigência do contrato.",
            "5. Fica proibida a sublocação ou cessão do imóvel sem consentimento prévio e por escrito do LOCADOR.",
            "6. Este contrato tem validade de 12 (doze) meses, podendo ser renovado mediante acordo entre as partes.",
            "7. Em caso de rescisão antecipada, a parte que desejar rescindir deverá notificar a outra com antecedência mínima de 30 (trinta) dias."
        ]

        for clausula in clausulas:
            pdf.multi_cell(0, 6, clausula)
            pdf.ln(2)

        pdf.ln(10)

        largura_assinatura = 80
        altura_assinatura = 10
        espacamento = 30

        x_inicial = pdf.get_x()
        y_inicial = pdf.get_y()

        pdf.line(x_inicial, y_inicial, x_inicial + largura_assinatura, y_inicial)
        pdf.line(x_inicial + largura_assinatura + espacamento, y_inicial,
                 x_inicial + 2 * largura_assinatura + espacamento, y_inicial)

        pdf.ln(5)

        pdf.set_x(x_inicial)
        pdf.cell(largura_assinatura, 10, "Locador", align="C")
        pdf.set_x(x_inicial + largura_assinatura + espacamento)
        pdf.cell(largura_assinatura, 10, "Locatário", align="C")

        pdf_file = "contrato_locacao.pdf"
        pdf.output(pdf_file)

        st.success("Contrato gerado com sucesso!")
        with open(pdf_file, "rb") as f:
            st.download_button(label="Baixar Contrato PDF", data=f, file_name=pdf_file)
