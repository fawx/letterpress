app.Games = Backbone.Collection.extend({
    url: '/api/games/',

    model: app.Game
});