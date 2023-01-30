# Documentação do funcionamento da interface

## Formulário

| Campo      | Descrição                   | Validação                                                                                                                           |
|------------|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Igreja     | Igreja da publicação        | Dropdown list, conforme arquivo de configuração                                                                                     |
| URL        | URL do vídeo                | http ou https no início                                                                                                             |
| Data       | Data da mensagem            | Se possível abrir um calendário para escolha                                                                                        |
| Turno      | Manhã/Tarde/Noite           | Campo opcional. Valores: "M, M1, M2, T, T1, T2, N, N1, N2, outro".<br/> No caso de outros, abrir uma opção para 2 caracteres        |
| Título     | Título da mensagem          | Sem validação                                                                                                                       |
| Pregador   | Nome do pregador            | Dropdown list, de acordo com a igreja, conforme arquivo de configuração.<br/>Pode existir opção de "outros", que abre um novo campo |
| Série      | Nome da série               | Dropdown list, de acordo com a igreja, conforme arquivo de configuração.<br/>Opção "Sem série" e "outros", que abre um novo campo   |
| Início     | Tempo do início da mensagem | Formato _hh:mm:ss_. Pode estar em branco                                                                                            |
| Fade in    | Opção de fade-in no áudio   | Check-box. Aparece quando o campo INICIO é preenchido                                                                               |
| Fim        | Tempo do fim da mensagem    | Formato _hh:mm:ss_. Pode estar em branco                                                                                            |
| Fade out   | Opção de fade-out no áudio  | Check-box. Aparece quando o campo FIM é preenchido                                                                                  |
| Comentário | Texto bíblico ou comentário | Opcional                                                                                                                            |

Também deve haver um campo de senha/chave no formulário, a senha é por igreja, baseada em arquivo de configuração.

## Arquivo de saída

Arquivo JSON com os campos preenchidos, lembrando que pode haver acentuação a caracteres UTF-8.

Nome do arquivo: ```YYYYMMDDTT-slug-pastor.json```

* **TT** é o turno, que pode ser nulo
* **Slug** é o _slug_ da igreja
* **Pastor** é o nome do pregador todo em minúsculas, com espaços substítuidos por "-". Não pode haver acentos e
caracteres especiais.

Gerar uma notificação _Telegram_ para quem preencheu. O número é baseado na igreja (arquivo de configuração)

A notificação deve ter o texto:
```text
[biblecast.net] Foi recebido para o tratamento o arquivo de áudio referente à mensagem de 
{DATA} com o título {TITULO}. Você receberá uma notificação quando essa mensagem foi publicada
com sucesso
```


## Arquivo de configuração

Arquivo JSON. Cada igreja tem um _slug_, que é uma string usada internamente. Esse _slug_ vai estar 
no arquivo de configuração.

* Nome das Igrejas
  * Nome das séries por igreja
  * Nome dos pastores por igreja
  * _slug_
  * Chave
  * Telefone(s) de envio via _Telegram_