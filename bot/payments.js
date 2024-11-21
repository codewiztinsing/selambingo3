const apiKey = "DEFAULT_af37ed09-7a87-4d0a-92d4-822ac4eb3642";
const baseUrl = "https://uat.api.addispay.et/checkout-api/v1";  //for uat
// const baseUrl = "https://api.addispay.et/checkout-api/v1";  //for main



const paymentData = {
  data: {
    redirect_url: "https://addispay.et/",
    cancel_url: "",
    success_url: "",
    error_url: "",
    order_reason: "Test payment for integration",
    currency: "ETB",
    email: "test@gmail.com",
    first_name: "Abebe",
    last_name: "Kebede",
    nonce: "testPay" + Date.now(),
    order_detail: {
      amount: 100,
      description: "test payment",
    },
    phone_number: "251921309013",
    session_expired: "5000",
    total_amount: "100",
    tx_ref: "testPay" + Date.now(),
  },
  message: "all in all good experience",
};

const createOrder = async (paymentData) => {
  const url = baseUrl + "/create-order";
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
      "Auth": apiKey,
    },
    body: JSON.stringify(paymentData),
  };

  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error("Order creation failed: " + errorText);
    }
    return await response.json();
  } catch (error) {
    console.error("Error creating order:", error.message);
    throw error;
  }
};

createOrder(paymentData)
  