app.Game = Backbone.Model.extend({
    defaults: {
        players: [],
        letters: [],
        played_out: [],
        turn: undefined,
        completed: false,
        play: [],
    },


    initialize: function() {
        // this.listenTo(this, 'change:owner', this.findSurrounded);
    },


    parse: function(response) {
        // backbone doesn't know that the array we're getting from the server actually
        // corresponds to a model definition, so let's remind it
        response.letters = new app.Letters(response.letters);
        
        // if we have more or less than 2 players, we're in trouble
        response.players[0] = new app.Player(response.players[0]);
        response.players[1] = new app.Player(response.players[1]);

        return response;
    }
});
