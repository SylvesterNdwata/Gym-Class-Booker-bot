retry(login, description="login")
retry(lambda: book_class("Tue", "6:00 PM"), description="booking classes")
retry(lambda: book_class("Thu", "6:00 PM"), description="booking classes")
retry(get_my_bookings, description="retrieving bookings")