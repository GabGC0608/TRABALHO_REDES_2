import { useEffect, useState } from "react";
import "./App.css";


function App() {

  const [username, setUsername] = useState("");
  const [inputName, setInputName] = useState("");

  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");

  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);



  useEffect(() => {

    const ws = new WebSocket(
      "ws://localhost:8765"
    );


    ws.onopen = () => {

      console.log("Conectado ao servidor");

      setConnected(true);

    };



    ws.onmessage = (event) => {


      const data = JSON.parse(event.data);


      setMessages((old)=>[

        ...old,

        {

          usuario: data.usuario,

          mensagem: data.mensagem,

          tipo:"received"

        }

      ]);


    };



    ws.onclose = () => {

      setConnected(false);

    };


    setSocket(ws);



    return () => {

      ws.close();

    };


  }, []);





  function entrarChat(){


    if(inputName.trim() !== ""){

      setUsername(inputName);

    }


  }






  function sendMessage(){


    if(
      message.trim() === "" ||
      !socket
    ){

      return;

    }



    const data = {


      usuario: username,


      mensagem: message


    };



    socket.send(
      JSON.stringify(data)
    );



    setMessages((old)=>[

      ...old,

      {

        usuario: username,

        mensagem: message,

        tipo:"sent"

      }

    ]);



    setMessage("");

  }





  return (


    <div className="page">



      {!username ? (


        <div className="login">


          <h1>
            💬 Chat WebSocket
          </h1>


          <input

            placeholder="Digite seu nome"

            value={inputName}


            onChange={(e)=>
              setInputName(e.target.value)
            }


          />



          <button onClick={entrarChat}>

            Entrar

          </button>



        </div>



      ) : (



      <div className="chat-container">


        <header>


          <h1>
            💬 Chat WebSocket
          </h1>


          <span className={
            connected
            ? "online"
            : "offline"
          }>


          {connected
            ? "● Online"
            : "● Offline"
          }


          </span>



          <p>

            Usuário: {username}

          </p>


        </header>





        <main className="messages">


          {messages.map((msg,index)=>(


            <div

              key={index}

              className={
                msg.tipo === "sent"
                ? "message sent"
                : "message received"
              }

            >


              <strong>

                {msg.usuario}

              </strong>


              <br/>


              {msg.mensagem}



            </div>



          ))}



        </main>





        <footer>


          <input


            value={message}


            onChange={(e)=>
              setMessage(e.target.value)
            }



            onKeyDown={(e)=>{


              if(e.key === "Enter"){

                sendMessage();

              }


            }}



            placeholder="Digite uma mensagem..."



          />




          <button onClick={sendMessage}>


            Enviar


          </button>



        </footer>




      </div>



      )}



    </div>



  );

}


export default App;