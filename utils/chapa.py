from chapa import Chapa


chapa = Chapa('CHASECK_TEST-vlw3GDzGJjCYI2GU9FDfInYk1L2t4KAk')

response = chapa.initialize(
    email="aleludago@gmail.com",
    amount=1000,
    first_name="Tinsae",
    last_name="Alak",
    tx_ref="fghj765jgg342q34fdasdfasdf34252345sdppfs",
    callback_url="https://selambingo.onrender.com/"
)
