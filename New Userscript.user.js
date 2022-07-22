// ==UserScript==
// @name         Lichess BOT
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Bot imbatible ajedrez
// @author       Víctor Pascual Muñoz
// @match        https://lichess.org/*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        none
// ==/UserScript==

(function() {
    /* PROBLEMAS
    *El principal problema era comunicar el Stockfish de python con el Javascript inyectado en la página

    *La idea inicial era hacer una API REST con el servidor de Python y hacer peticiones desde el script inyectado para realizar los movimientos
    pero debido a la etiqueta HTML META http-equiv="Content-Security-Policy" y su valor "connect-src 'self' lichess1.org wss://socket0.lichess.org" no pude hacer la conexión,
    intente eliminarla antes de que cargará el DOM y varias cosas más, pero no surtia efecto nada.

    *Asi que intente utilizar los datos que almacenaba el propio navegador en el ordenados (cookies(no se actualizan inmediatamente), localStorage(encriptado) y bases de datos SQLite)
    opte por SQLite, y python accedia a los movimientos hechos por el oponente a traves del SQLite
    */

    //localStorage.setItem('miGato', 'Juan');
    //document.cookie = "move2e4=";
    var contador = 1;
    var myDBInstance = openDatabase('LichessBot', '1.0', 'This is a client side database', 2 * 1024 * 1024);
    if (!myDBInstance) {
        alert('Oops, your database was not created');
    }
    else {
        var version = myDBInstance.version;
         myDBInstance.transaction(function (tran) {
        tran.executeSql('CREATE TABLE IF NOT EXISTS Move (id unique, move)');
        tran.executeSql('DELETE FROM Move;');
    });
    }
    var OrigWebSocket = window.WebSocket;
    var callWebSocket = OrigWebSocket.apply.bind(OrigWebSocket);
    var wsAddListener = OrigWebSocket.prototype.addEventListener;
    wsAddListener = wsAddListener.call.bind(wsAddListener);
    window.WebSocket = function WebSocket(url, protocols) {
        var ws;
        if (!(this instanceof WebSocket)) {
            ws = callWebSocket(this, arguments);
        } else if (arguments.length === 1) {
            ws = new OrigWebSocket(url);
        } else if (arguments.length >= 2) {
            ws = new OrigWebSocket(url, protocols);
        } else {
            ws = new OrigWebSocket();
        }

        wsAddListener(ws, 'message', function(event) {
            // CADA VEZ QUE EL SOCKET RECIBE DATOS
            let datos_recibidos = JSON.parse(event.data);
            if(datos_recibidos.t == "move"){
                console.log(datos_recibidos.d.uci)
                myDBInstance.transaction(function (tran) {
                    tran.executeSql('insert into Move (id ,move) values ('+ contador++ +', "'+datos_recibidos.d.uci+'")');
                });
            }
        });
        return ws;
    }.bind();
    window.WebSocket.prototype = OrigWebSocket.prototype;
    window.WebSocket.prototype.constructor = window.WebSocket;

    var wsSend = OrigWebSocket.prototype.send;
    wsSend = wsSend.apply.bind(wsSend);
    OrigWebSocket.prototype.send = function(data) {
        // Esto era para modificar los datos deel socket y modificar el movimiento
        let datos = JSON.parse(data);
        //datos.d.u = "h2h3"
        //data = JSON.stringify(datos)
        return wsSend(this, arguments);
    };


    setInterval(function(){
    //CODIGO QUE SE EJECUTA CADA SEGUNDO (ESTO NO SIRVE PARA NADA AL FINAL)
        myDBInstance.transaction(function (tran) {
            tran.executeSql('SELECT * FROM Move', [], function (tx, results) {
                var len = results.rows.length, i;
                var currentMove = results.rows.item(len-1)
                if(contador - 1 == currentMove.id){
                    console.log("sin movimientos detectados")
                }else{
                    console.log("movimiento detectado")
                }
            }, null);

        });
    }, 1000);
})();