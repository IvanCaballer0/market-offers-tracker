from dotenv import load_dotenv
from playwright.async_api import async_playwright

import argparse
import asyncio
import client_ollama
import client_nvidia
import json
import os
import sys


async def go_website(page, url):
    try:
        print(f"Navegando al sitio web {url} ...")

        await page.goto(url)
        await asyncio.sleep(10)

        print("Se cargo correctamente el sitio web.")
    except Exception as e:
        print(f"Ocurrio un error en la funcion 'go_website'. Error: {e}")


async def check_login(page):
    try:
        print("Iniciando sesión...")

        return await page.locator("a[title='Ivan Caballero']").count() > 0
    except Exception as e:
        print(f"Ocurrio un error en la funcion 'check_login'. Error: {e}")


async def sign_in(page):
    try:
        if await check_login(page):
            print("Se inicio sesion correctamente.")
            return

        # Inicializar credenciales
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")

        # Dar clic en el botón "Ingresa".
        await page.wait_for_selector("a[href='https://www.workana.com/es/login']")
        await page.click("a[href='https://www.workana.com/es/login']")
        await asyncio.sleep(10)

        # Llenar el formulario.
        await page.wait_for_selector("input[id='email-input']")
        await page.fill("input[id='email-input']", email)
        await asyncio.sleep(3)
        await page.wait_for_selector("input[id='password-input']")
        await page.fill("input[id='password-input']", password)
        await asyncio.sleep(3)
        await page.click("button[type='submit']")
        await asyncio.sleep(10)

        if await page.locator("a[title='Ivan Caballero']").count() > 0:
            print("Se inicio sesion correctamente.")
        else:
            print("Ocurrio un error al iniciar sesión.")
    except Exception as e:
        print(f"Ocurrio un error en la funcion 'view_offers'. Error: {e}")


async def view_offers(page):
    try:
        print("Navegando a las ofertas...")

        await page.wait_for_selector("a[href='https://www.workana.com/jobs']")
        await page.click("a[href='https://www.workana.com/jobs']")
        await asyncio.sleep(10)

        print("Ofertas cargadas correctamente.")
    except Exception as e:
        print(f"Ocurrio un error en la funcion 'sign_in'. Error: {e}")


async def select_filter(page):
    try:
        print("Seleccionando el filtro de búsqueda...")

        await page.click(".multi-select-selection")
        await page.wait_for_selector("span:has-text('Recurrente')", state="visible")
        await page.click("span:has-text('Recurrente')")
        await asyncio.sleep(3)

        print("Filtro seleccionado con éxito.")
    except Exception as e:
        print(f"Ocurrio un error en la funcion 'select_filter'. Error: {e}")


async def submit_proposal(page, decision_made):
    try:
        print("Enviando la propuesta al enunciado...")

        await page.wait_for_selector("#bid_button")
        await page.click("#bid_button")

        await page.wait_for_selector("#bidForm")
        await asyncio.sleep(10)

        await page.wait_for_selector("#Amount")
        await page.fill("#Amount", str(decision_made.get("budget")))
        await asyncio.sleep(3)

        await page.wait_for_selector("#BidContent")
        await page.fill("#BidContent", decision_made.get("project_proposal"))
        await asyncio.sleep(3)

        await page.wait_for_selector("#BidDeliveryTime")
        await page.fill("#BidDeliveryTime", decision_made.get("development_time"))
        await asyncio.sleep(3)

        await page.wait_for_selector("input[value='Enviar presupuesto']")
        await page.click("input[value='Enviar presupuesto']")

        await page.wait_for_selector("#container")
        await asyncio.sleep(10)

        print("Se envio la propuesta correctamente.")
    except Exception as e:
        print(f"Ocurrio un error en la funcion 'submit_proposal'. Error: {e}")


async def evaluate_statement(page, data, lst, model):
    try:
        application_response = model.evaluate_statement(data)
        if application_response is not None:
            decision_made = json.loads(application_response)

        if decision_made.get("apply") is True:
            print(f"Se aprobo el proyecto.")
            await submit_proposal(page, decision_made)
        elif decision_made.get("apply") is False:
            print(f"Proyecto descartado.")
            print(decision_made.get("project_proposal"))

        lst.append(data["title"].lower())

        with open("proposals.txt", "a", encoding="utf-8") as f:
            f.write(f"{data["title"].lower()}\n")

        await asyncio.sleep(10)
    except Exception as e:
        print(f"Ocurrio un error en la funcion 'evaluate_statement'. Error: {e}")


async def get_statement(page, browser, list_proposal, model):
    try:
        await page.wait_for_selector(".project-item")
        statements = await page.locator(".project-item").all()

        path_tag = ".project-header .project-title span a"

        for statement in statements:
            print("=" * 105)

            tag = statement.locator(path_tag)
            partial_url = await tag.get_attribute("href")
            url = "https://www.workana.com" + partial_url

            page_statement = await browser.new_page()
            await go_website(page_statement, url)

            container = page_statement.locator(".project-view-v3")

            tag_title = container.locator("h1.title")
            title = await tag_title.evaluate(
                "(el) => el.childNodes[0].textContent.trim()"
            )
            title = title.lower()

            budget_container = container.locator("h4.budget")
            budget = await budget_container.inner_text()

            information_container = container.locator("div.expander")
            information = await information_container.inner_text()

            delivery_date_container = await container.locator("p.mt20").all()
            for item_delivery_date in delivery_date_container:
                delivery_date = await item_delivery_date.inner_text()
                if "Plazo de Entrega" in delivery_date:
                    delivery = delivery_date.split(":")[1].strip()
                    break
                elif "Duración del proyecto" in delivery_date:
                    delivery = "No definido"
                    break

            skills_container = await container.locator("a.skill").all()
            skills_list = []
            for skill_container in skills_container:
                skill = await skill_container.get_attribute("title")
                skills_list.append(skill.replace("Trabajos Freelance de ", ""))

            if title not in list_proposal:
                data_statement = {
                    "title": title,
                    "budget": budget,
                    "information": information,
                    "delivery": delivery,
                    "skills": skills_list,
                }

                await evaluate_statement(
                    page_statement, data_statement, list_proposal, model
                )
            else:
                print(f"El enunciado '{title}' ya fue evaluado.")

            await page_statement.close()
        print("Ya se recorrierón todos los enunciados de la primera pagina.")
    except Exception as e:
        print(f"Ocurrio un error en la funcion 'get_statement'. Error: {e}")


async def main(model):
    try:
        async with async_playwright() as p:
            # Inicializar lista de propuestas.
            list_proposal = []
            with open("proposals.txt", "r", encoding="utf-8") as f:
                for row in f:
                    list_proposal.append(row.strip())

            # Inicializar navegador.
            browser = await p.chromium.launch_persistent_context(
                user_data_dir="./workana_profile", headless=False
            )
            page = await browser.new_page()

            # 1. Navegar al sitio web.
            await go_website(page, "https://www.workana.com/es")

            # 2. Iniciar sesión.
            await sign_in(page)

            # 3. Visualizar los enunciados.
            await view_offers(page)

            # 4. Escoger los filtros de busqueda.
            await select_filter(page)

            # 5. Obtener y evaluar los enunciados.
            await get_statement(page, browser, list_proposal, model)

            await asyncio.sleep(300)

            await browser.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        add_help=False
    )

    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Muestra el menu de ayuda."
    )

    parser.add_argument(
        "-m",
        "--model",
        metavar="str",
        help="Selecciona el modelo 'local' o 'cloud'."
    )

    args = parser.parse_args()

    if args.model == "local":
        model = client_ollama
    elif args.model == "cloud":
        model = client_nvidia
    else:
        print("Seleccione un modelo valido. (client_ollama ó client_nvidia).")
        sys.exit(1)

    load_dotenv()
    asyncio.run(main(model))
