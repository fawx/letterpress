app.Games = Backbone.Collection.extend({
    url: '/games/api/',

    model: app.Game
});