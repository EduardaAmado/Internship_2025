from smtplib import SMTP
from email.message import EmailMessage
import mysql.connector

def get_email_sender():
    # Conectar ao banco de dados para obter o remetente
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="smb_notifications"  # Alterado para a nova base de dados
    )
    
    cursor = mydb.cursor()
    cursor.execute("SELECT email FROM sender")  # Alterado para selecionar a coluna correta
    rows = cursor.fetchall()
    
    cursor.close()
    mydb.close()
    
    return rows[0][0] if rows else None  # Retorna o primeiro remetente, se existir

def get_email_receivers():
    # Conectar ao banco de dados para obter os destinatários
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="smb_notifications"  # Alterado para a nova base de dados
    )
    
    cursor = mydb.cursor()
    cursor.execute("SELECT email FROM receivers")  # Selecionar todos os destinatários
    rows = cursor.fetchall()
    
    cursor.close()
    mydb.close()
    
    return [row[0] for row in rows]  # Retorna uma lista de todos os e-mails dos destinatários

def send_email(receiver_email, subject, body):
    sender_email = get_email_sender()
    
    if not sender_email:
        print("Sender email not found")
        return
    
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Importance'] = 'High'
    
    message.set_content(body)

    # Enviar o e-mail
    try:
        with SMTP('srvsmtp') as server:
            server.send_message(message)
            print("E-mail enviado com sucesso para", receiver_email)
    except Exception as e:
        print("Falha ao enviar o e-mail:", e)

def main():
    subject = "Atualização do AnyWhere / AnyWhere Update"
    
    # Adicione o link do AnyWhere aqui
    anywhere_link = "https://anywhere.d.bbg/hello"  # Substitua pelo link real

    body_pt = (
        "Olá,\n\n"
        "Este é um lembrete para que você atualize o AnyWhere para garantir que "
        "você tenha acesso às últimas funcionalidades e melhorias de segurança.\n"
        f"Por favor, verifique a versão mais recente e atualize o quanto antes: {anywhere_link}\n\n"
        "Obrigado!\n"
        "Equipe de Suporte"
    )
    
    body_en = (
        "Hello,\n\n"
        "This is a reminder for you to update AnyWhere to ensure that "
        "you have access to the latest features and security improvements.\n"
        f"Please check for the latest version and update as soon as possible: {anywhere_link}\n\n"
        "Thank you!\n"
        "Support Team"
    )

    # Combine both bodies into one message
    body = f"{body_pt}\n\n---\n\n{body_en}"

    receiver_emails = get_email_receivers()  # Obter todos os destinatários
    
    # Usar um conjunto para garantir que os e-mails sejam únicos
    unique_emails = set(receiver_emails)
    
    for receiver_email in unique_emails:
        send_email(receiver_email, subject, body)  # Enviar e-mail para cada destinatário

if __name__ == "__main__":
    main()
