var Verification = {
    list: [],
    loadList: function() {
        return m.request({
            method: "GET",
            url: "api/v1/order-verification",
            headers: {
                Authorization: dsa.acess_token()
            },
            withCredentials: true,
        })
        .then(function(result) {
            Verification.list = result.data
            console.log(Verification.list)
        })
    }
}