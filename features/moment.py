from features.feature import Feature;

class Moment( Feature ):
    def __init__( self, cout, env, req ):
        super().__init__( cout, env );
        self.category = env.datasets.content[ req ];
        cout.comment( self.category );