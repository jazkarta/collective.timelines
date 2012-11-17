from zope.schema.vocabulary import SimpleVocabulary
from collective.timelines import timelinesMessageFactory as _


ANNOTATION_KEY = 'collective.timelines.annotation'

MAP_STYLES = (
    (u'ROADMAP', _(u'Google Maps: Roadmap')),
    (u'SATELLITE', _(u'Google Maps: Satellite')),
    (u'HYBRID', _(u'Google Maps: Hybrid')),
    (u'TERRAIN', _(u'Google Maps: Terrain')),
    (u'watercolor', _(u'Stamen Maps: Watercolor')),
    (u'toner', _(u'Stamen Maps: Toner')),
    (u'toner-lines', _(u'Stamen Maps: Toner Lines')),
    (u'toner-labels', _(u'Stamen Maps: Toner Labels')),
    (u'sterrain', _(u'Stamen Maps: Terrain')),
    )

FONT_CHOICES = (
    (u'Georgia-Helvetica', _(u'Georgia & Helvetica Neue')),
    (u'Bevan-PotanoSans', _(u'Bevan & Potano Sans')),
    (u'Merriweather-NewsCycle', _(u'Merriweather & News Cycle')),
    (u'NewsCycle-Merriweather', _(u'News Cycle & Merriweather')),
    (u'PoiretOne-Molengo', _(u'Poiret One & Molengo')),
    (u'Arvo-PTSans', _(u'Arvo & PT Sans')),
    (u'PTSerif-PTSans', _(u'PT Serif & PT Sans')),
    (u'DroidSerif-DroidSans', _(u'Droid Serif & Droid Sans')),
    (u'Lekton-Molengo', _(u'Lekton & Molengo')),
    (u'NixieOne-Ledger', _(u'Nixie One & Ledger')),
    (u'AbrilFatface-Average', _(u'Abril Fatface & Average')),
    (u'PlayfairDisplay-Muli', _(u'Playfair Display & Muli')),
    (u'Rancho-Gudea', _(u'Rancho & Gudea')),
    (u'BreeSerif-OpenSans', _(u'Bree Serif & Open Sans')),
    (u'SansitaOne-Kameron', _(u'Sansita One & Kameron')),
    (u'Pacifico-Arimo', _(u'Pacifico & Arimo')),
    (u'PT', _(u'PT Sans & PT Narrow & PT Serif')),
    )

MAP_VOCAB = SimpleVocabulary([SimpleVocabulary.createTerm(t[0],
                                                          t[0].encode('ascii'),
                                                          t[1])
                              for t in MAP_STYLES])
FONT_VOCAB = SimpleVocabulary([SimpleVocabulary.createTerm(t[0],
                                                           t[0].encode('ascii'),
                                                           t[1])
                               for t in FONT_CHOICES])
