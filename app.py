import gradio as gr
import random
import time
import websocket,json

ws=websocket.create_connection('wss://hack.chat/chat-ws')

with gr.Blocks() as demo:
    _chat_history=None
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    mynick = gr.Textbox(label='Nick first')

    def respond(message, chat_history):
        global _chat_history
        ws.send(json.dumps({'cmd':'chat','text':message}))
        chat_history.append((message,None))
        _chat_history=chat_history
        return "", chat_history
        
    def join(nick):
        ws.send(json.dumps({'cmd':'join','nick':nick,'channel':'your-channel'}))
        return None


    def get_plot(mynick,chat_history):
        data=json.loads(ws.recv())

        if data['cmd']=='chat':
            nick=data['nick']
            if nick==mynick:
                print('hm')
                return _chat_history
            text=data['text']
            trip=data.get('trip')
            _text=str(trip)+' '+nick+':\n'+text
            chat_history.append(( None,_text))

        elif data['cmd']=='onlineAdd':
            nick=data['nick']
            trip=data.get('trip')
            _text='* '+str(trip)+' '+nick+' joined'
            chat_history.append(( None,_text))

        elif data['cmd']=='onlineRemove':
            nick=data['nick']
            _text='* '+nick+' left'
            chat_history.append(( None,_text))

        elif data['cmd']=='updateUser':
            nick=data['nick']
            _text='* '+nick+' updated'
            chat_history.append(( None,_text))

        elif data['cmd']=='warn':
            text=data['text']
            _text='! '+text
            chat_history.append(( None,_text))

        elif data['cmd']=='info':
            text=data['text']
            _text='** '+text
            chat_history.append(( None,_text))

        elif data['cmd']=='emote':
            text=data['text']
            _text='*** '+text
            chat_history.append(( None,_text))

        else:
            chat_history.append(( None,json.dumps(data)))

        return chat_history


    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    mynick.submit(join, mynick, None, queue=False)
    dep = demo.load(get_plot, [mynick,chatbot], chatbot, every=1)



if __name__ == "__main__":
    demo.queue().launch()

