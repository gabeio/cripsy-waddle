var mvvm = function () {
    window.mvvm = this
    var self = this
    this.container = ko.observable("empty") // which template is loaded
    this.song_list = ko.observableArray([])
    this.songs = class {
        create(callback, title, uri) {
            // title (required)
            // uri (required)
            $.ajax({
                url: '/api/v0/songs',
                type: 'POST',
                data: {
                    title: title,
                    uri: uri
                },
                success: function(result) {
                    console.log('POST > '+result)
                    callback(null, JSON.parse(result))
                }
            })
        }
        get(callback, id) {
            // id (optional)
            if (typeof id == 'undefined') {
                this.id = ''
            } else {
                this.id = '/' + id
            }
            $.ajax({
                url: '/api/v0/songs'+this.id,
                type: 'GET',
                success: function(result) {
                    console.log('GET > ' + result)
                    callback(null, JSON.parse(result))
                }
            })
        }
        update(callback, id) {
            // id (required)
            $.ajax({
                url: '/api/v0/songs/'+id,
                type: 'PUT',
                data: {
                    title: title,
                    uri: uri
                },
                success: function(result) {
                    console.log('PUT > '+result)
                    callback(null, JSON.parse(result))
                }
            })
        }
        delete(callback, id) {
            // id (required)
            $.ajax({
                url: '/api/v0/songs/'+id,
                type: 'DELETE',
                success: function(result) {
                    console.log('DELETE > '+result)
                    callback(null, JSON.parse(result))
                }
            })
        }
        vote(song) {
            console.log("vote started")
            $.ajax({
                url: '/api/v0/votes/'+song.id,
                type: 'PUT',
                success: function(result) {
                    console.log('PUT > ' + result)
                    callback(null, JSON.parse(result))
                }
            })
        }
    }
    this.song_list_sort = function () {
        self.song_list.sort(function(l,r) {
            id = null
            if (l.score == r.score) {
                return 0
            } else {
                if (l.score > r.score) {
                    return -1
                } else {
                    return 1
                }
            }
        })
    }

    async.parallel([
        // function(callback) {
        //     song = new self.songs();
        //     song.create(callback, "test", "example")
        // },
        function(callback) {
            song = new self.songs();
            song.get(function(error, res) {
                for (var i=0; i < res.length; i++) {
                    self.song_list.push(res[i])
                }
                self.song_list_sort()
                callback(error)
            })
        },
        function (callback) {
            callback(null)
        }
    ], function(err, res) {
        console.log("complete")
        self.container("home")
    })

} ()
ko.applyBindings(mvvm)
