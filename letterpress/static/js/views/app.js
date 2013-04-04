app.AppView = Backbone.View.extend({
    el: '.letterpress-app',


    subviews: {
        player: undefined,
        games: undefined,
    },


    initialize: function() {
        this.subviews.player = new app.PlayerView({ 
            model: new app.Player(), 
            el: '#player-info' 
        });

        this.subviews.games = new app.GamesView({ 
            collection: new app.Games(),
            el: '#games',
        });
    },


    get_current_player: function() {
        return this.subviews.player.model.get('username');
    },
});
