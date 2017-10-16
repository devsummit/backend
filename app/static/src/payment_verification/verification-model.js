var Verification = {
    list: [],
    current: {},
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
        })
    },
    save: function() {
        return m.request({
            method: "POST",
            url: "api/v1/order-verification/" + Verification.current.id + "/verify",
            headers: {
                Authorization: dsa.acess_token()
            },
            withCredentials: true,
        })
        .then(function(result) {
            if(result.meta.success) {
                alert('Verification success tiket have been created!')
                Verification.current.is_used = true
            }
        })
    }
}