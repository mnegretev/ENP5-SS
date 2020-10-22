#!/usr/bin/env python

import rospy  #Esta linea la hicieron bien
from geometry_msgs.msg import Twist  #Esta linea es la que debe ir en lugar del 'import rostopic'

def girador():
    print("Initializing simple move node ...") #Siempre es conveniente imprimir algo en pantall para saber que el programa ya inicio.
    rospy.init_node('girador', anonymous=True) #Esta linea la hicieron bien, pero el init_node siempre debe ir antes
                                               #de declarar cualquier publicador o suscriptor.
                                               
    #Esta linea si tenia varios problemas:
    #El primer argumento estaba bien, que corresponde al nombre del topico
    #El segundo argumento es el 'tipo' del topico, es decir, un Twist, pero tenian que hacer el 'import' correcto.
    #El ultimo argumento NO es el dato que se desea publicar. Corresponde a una estructura llamada Queue que
    #estudiaran en los primeros semestres si es que estudian algo relacionado con computacion.
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    #Ahora, para que el robot se mueva, es necesario publicar periodicamente el valor de la velocidad mediante un Twist.
    #Para eso vamos a usar un ciclo While con un retraso dentro.
    loop = rospy.Rate(10)  #Esta linea crea un temporizador que me va a dar un retraso de mas o menos 100 ms (o sea, 10 Hz)
    #Uso un ciclo while que revisa si no se ha recibido una senal de terminar programa:
    while not rospy.is_shutdown():
        cmd_vel = Twist()        #Esta linea crea un nuevo objeto de tipo Twist
        cmd_vel.angular.z = 0.5  #Fijo la velocidad angular en 0.5 rad/seg
        pub.publish(cmd_vel)     #Esta es la linea que va a realizar el envio del twist.
        loop.sleep()# Esta linea es la que produce un retraso de 100 ms, lo que hara que la velocidad se publique 10 veces por segundo.
        
if __name__ == '__main__':
    try:
        girador()
    except rospy.ROSInterruptException:
        pass
        
