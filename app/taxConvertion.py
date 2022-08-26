from typing import Dict

def estimacion_intereses(tipo: int, interes: float, periodo: float) -> Dict:
    """
    #1 -> CONVERSION DE INTERES NOMINAL VENCIDO A EFECTIVO ANUAL
    #2- > CONVERSION DE INTERES NOMINAL ANTICIPADO A EFECTIVO ANUAL
    #3 -> CONVERSION DE INTERES EFECTIVO ANUAL A NOMINAL VENCIDO
    #4 -> CONVERSION DE INTERES EFECTIVO ANUAL A NOMINAL ANTICIPADO

    Args:
        tipo (int): _description_
        interes (float): _description_
        periodo (float): _description_

    Returns:
        Dict: _description_
    """
    
    if tipo == 1:
        return {
                'status': 200,
                'resultado': round(((1 + (interes/periodo)) ** periodo) - 1, 4), 
                'incial': 'CONVERSION DE INTERES NOMINAL VENCIDO A EFECTIVO ANUAL',
                'concepto': 'Interes efectivo anual'
                }
    elif tipo == 2:
        return {
                'status': 200,
                'resultado': round((1 / ((1 - (interes/periodo)) ** periodo) - 1), 4), 
                'incial': 'CONVERSION DE INTERES NOMINAL ANTICIPADO A EFECTIVO ANUAL',
                'concepto': 'Interes efectivo anual'
                }
    elif tipo == 3:
        return {
                'status': 200,
                'resultado': round(((1+interes) ** (1/periodo) - 1) * periodo, 4), 
                'incial': 'CONVERSION DE INTERES EFECTIVO ANUAL A NOMINAL VENCIDO',
                'concepto': 'Interes nominal vencido'
                }
    elif tipo == 4:
        return {
                'status': 200,
                'resultado': round((1-(1/(1+interes)) ** (1/periodo)) * periodo, 4) , 
                'incial': 'CONVERSION DE INTERES EFECTIVO ANUAL A NOMINAL ANTICIPADO',
                'concepto': 'Interes nominal anticipado'
                }
        
    return {
            'status': 400, 
            'resultado': 'No Aplica',
            'incial': 'No Aplica',
            'concepto': 'No Aplica' 
            }
    
if __name__ == '__main__':
    resultado = estimacion_intereses(tipo = 1, interes = 0.14, periodo = 4)
    print(resultado)