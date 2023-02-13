# PS-Python-React-JACKSON

Somente foi entregue o backend.
Não pude containizar a tempo.

O projeto foi feito totalmente tipado.

Com autenticação feita em jwt para casos onde o servidor não consegue ultilizar o a autenticação do proprio Django, por exmplo servidores do pythonanywhere.

Resolvi deixar o sistema de precos e frete no app de pagamentos, já que se fosse em uma aplicacao real o app de pagamento seria um microservico separado, então para evitar problemas com informações de precos diferentes.

Como rodar o backend:
- Va ate Backend/api
- Abra o arquivo '.env'
- Configure as variaveis conforme seu database
- Abra o prompt de comando
- Digite 'pip install -r requirements.txt'
- Digite 'python populate_database.py'
- Digite 'python manage.py runserver'

A Api tambem é documentada usando swagger, para acessar digite em seu navegador: http://127.0.0.1:8000/swagger/

EndPoints:
<br></br>

  Games:
  <br></br>
    http://127.0.0.1:8000/games/ - ['GET'] - mostra a lista de todos os jogos no database
    <br></br>
    http://127.0.0.1:8000/games/(game_id)/  - ['GET'] - mostra um jogo
    <br></br>
    
  User:
  <br></br>
    http://127.0.0.1:8000/user/ - ['GET'] - mostra as informaçoes do usuario logado
    <br></br>
    http://127.0.0.1:8000/user/ - ['POST'] - loga o usuario
    <br></br>
    http://127.0.0.1:8000/user/ - ['PUT'] - cria um novo usuario
    <br></br>
 
  Cart:
  <br></br>
    http://127.0.0.1:8000/cart/ - ['GET'] - mostra todos os jogos no carrinho do usuario logado
    <br></br>
    http://127.0.0.1:8000/cart/ - ['DELETE'] - remove jogos do carrinho do usuario logado
    <br></br>
    http://127.0.0.1:8000/cart/ - ['POST'] - adiciona jogos ao carrinho do usuario logado
    <br></br>
    <br></br>
    
  Price Checker:
  <br></br>
    http://127.0.0.1:8000/price-checker/ - ['GET'] - pega o valor total do jogos no carrinho do usuario logado, usando sistema de frete
    <br></br>
    
  Payment:
  <br></br>
    http://127.0.0.1:8000/payment/ - ['POST'] - ega o valor total do jogos no carrinho do usuario, usando sistema de frete, faz o pagamento e esvazia o carrinho do usuario logado
