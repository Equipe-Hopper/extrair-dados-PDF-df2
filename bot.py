from modules.email import Email
from modules.pdf import Pdf
from botcity.web import WebBot, Browser, By
from botcity.maestro import *

BotMaestroSDK.RAISE_NOT_CONNECTED = False

class Bot(WebBot):

    def action(self=None,execution=None):
        maestro = BotMaestroSDK.from_sys_args()
        execution = maestro.get_execution()

        print(f"Task ID is: {execution.task_id}")
        print(f"Task Parameters are: {execution.parameters}")

        try:
            maestro.alert(
                task_id=execution.task_id,
                title="Iniciando automação",
                message="A automaçao foi iniciada...",
                alert_type=AlertType.INFO
            )

            # Executar a extração e envio de e-mail
            email = Email()
            pdf = Pdf()
            output_file = pdf.extract_phone_numbers('resources\Telefone.pdf')
            if output_file is not None:
                email.send_email_with_attachment(output_file)

            finshed_status = AutomationTaskFinishStatus.SUCCESS

            finish_message = "Tarefa finalizada com sucesso"

        except Exception as ex:
            print("Error: ", ex)
            self.save_screenshot("resources/erro.png")

            finshed_status = AutomationTaskFinishStatus.FAILED
            finish_message = "Tarefa finalizada com erro"
        
        finally:
            self.wait(3000)
            # maestro.alert(
            #     task_id= execution.task_id,
            #     title= "Finalizou automação",
            #     message= "This is an info alert",
            #     alert_type= AlertType.INFO
            # )
            maestro.finish_task(
                task_id=execution.task_id,
                status=finshed_status,
                message=finish_message
            )

    def not_found(self, label):
        print(f"Element not found: {label}")

if __name__ == "__main__":
    Bot.main()