#Ficheiro .py apresentação da aplicação
#Biblioteca
#-----------
import os
import time
import threading
import customtkinter as ctk
from users import *

def openSplash(app):
    """
    
    """
    splash=ctk.CTkToplevel(app)
    splash.title("Your Joining the App")
    splash.geometry("1200x675")
    splash.configure(bg = "#121212")

    return splash

def openLogin(app,screen):
    """
    
    """
    screen.destroy()

    app.deiconify()
    app.geometry("1200x675")
    app.configure(bg="#E6F2F0")
    app.title("Hoot - Iniciar Sessão")

    def relative_to_assets(path: str):
        return f"./assets/{path}"

    # Email
    email_label = ctk.CTkLabel(
        app,
        text="E-MAIL",
        font=("Helvetica Bold", 10),
        text_color="#000000"
    )
    email_label.place(x=513, y=92)

    email_entry = ctk.CTkEntry(
        app,
        placeholder_text="Enter your email",
        fg_color="#D9D9D9",
        text_color="#000716",
        width=435,
        height=41,
    )
    email_entry.place(x=521, y=110)

    # Password
    password_label = ctk.CTkLabel(
        app,
        text="PALAVRA-PASSE*",
        font=("Helvetica Bold", 10),
        text_color="#000000"
    )
    password_label.place(x=513, y=173)

    password_entry = ctk.CTkEntry(
        app,
        placeholder_text="Enter your password",
        fg_color="#D9D9D9",
        text_color="#000716",
        show="*",
        width=435,
        height=41,
    )
    password_entry.place(x=521, y=191)

    # "Esqueceste-te da tua palavra passe?" Label
    forgot_password_label = ctk.CTkLabel(
        app,
        text="Esqueceste-te da tua palavra passe?",
        font=("Helvetica", 15),
        text_color="#4F8377"
    )
    forgot_password_label.place(x=513, y=246)

    #Login
    login_button = ctk.CTkButton(
        app,
        text="Iniciar Sessão",
        command=lambda: print("button_1 clicked"),
        width=173,
        height=36,
    )
    login_button.place(x=513, y=297)

    #Section
    section_title = ctk.CTkLabel(
        app,
        text="Iniciar Sessão",
        font=("Helvetica Bold", 24),
        text_color="#4F8377"
    )
    section_title.place(x=513, y=36)

    # Footer
    footer_title = ctk.CTkLabel(
        app,
        text="Ainda não tens conta?",
        font=("Helvetica Bold", 24),
        text_color="#4F8377"
    )
    footer_title.place(x=513, y=494)

    footer_text1 = ctk.CTkLabel(
        app,
        text="Se ainda não tens conta, cria aqui e começa a tirar partido das melhores ",
        font=("Helvetica Bold", 16),
        text_color="#121212",
        wraplength=400
    )
    footer_text1.place(x=514, y=540)

    footer_text2 = ctk.CTkLabel(
        app,
        text="vantagens na Hoot.",
        font=("Helvetica Bold", 16),
        text_color="#121212"
    )
    footer_text2.place(x=514, y=565)

    # Sign Up Button
    signup_button = ctk.CTkButton(
        app,
        text="Criar Conta",
        command=lambda: logIn(),
        width=173,
        height=36,
    )
    signup_button.place(x=513, y=601)

    # Sidebar Text
    sidebar_text1 = ctk.CTkLabel(
        app,
        text="A tua biblioteca ",
        font=("Helvetica Bold", 34),
        text_color="#E6F2F0"
    )
    sidebar_text1.place(x=93, y=351)

    sidebar_text2 = ctk.CTkLabel(
        app,
        text="de filmes",
        font=("Helvetica Bold", 34),
        text_color="#E6F2F0"
    )
    sidebar_text2.place(x=93, y=393)

    sidebar_text3 = ctk.CTkLabel(
        app,
        text="e séries",
        font=("Helvetica Bold", 34),
        text_color="#E6F2F0"
    )
    sidebar_text3.place(x=93, y=435)

    # Placeholder for Image (if required)
    image_placeholder = ctk.CTkLabel(
        app,
        text="[Your Image Here]",
        font=("Helvetica Bold", 20),
        text_color="#000000",
        width=250,
        height=250,
        fg_color="#D9D9D9"
    )
    image_placeholder.place(x=234 - 125, y=337 - 125)  # Centering placeholder


def waitSimulation(app,screen):
    """
    Espera 3 segundos antes de apresentar o proximo ecrã
    """
    time.sleep(3)
    app.after(0, lambda: openLogin(app, screen))

def main():
    """
    Função principal de funcionamento da app
    """
    app= ctk.CTk()#Inicia a App
    app.withdraw()#Esconde a janela

    #Criar a Splash Screen
    splashScreen = openSplash(app)

    #Inicia o Loading
    threading.Thread(target=lambda: waitSimulation(app, splashScreen), daemon=True).start()

    app.mainloop()
    

main()