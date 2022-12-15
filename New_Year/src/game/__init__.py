from typing import Callable

Command = Callable[[], None]

# Candle Texts
CANDLE_TOP_TEXT_DOWN = 'Вы подошли к свече, которая не горит.'
CANDLE_COME_UP_LOWERED_TEXT = 'Вы подошли к свече, которая как-то потухла.'
CANDLE_COME_UP_RAISED_TEXT = 'Вы подошли к свече, которая как-то зажглась.'
CANDLE_COME_UP_UP_TEXT = 'Вы подошли к свече, которая просто горит.'
CANDLE_COME_UP_UNKNOWN_TEXT = 'Вы подошли к свече, с которой фиг знает что.'

CANDLE_RESET_EFFECT_TEXT = 'Вытереть свечу рукавом.'
CANDLE_RESET_EFFECT_RESULT_TEXT = 'Вы вытерли фетиль свечи и теперь он сухой.',
CANDLE_BLOW_OUT_TEXT = 'Просто потушить свечу.',
CANDLE_BLOW_OUT_RESULT_TEXT = 'Вы потушили свечу.'
CANDLE_LIGHT_UP_TEXT = 'Зажечь свечу.'
CANDLE_LIGHT_UP_RESULT_TEXT = 'Вы зажгли свечу.'
CANDLE_WET_TEXT = 'Намочить свечу.'
CANDLE_WET_RESULT_TEXT = 'Вы слегка намочили свечу.'

# Fireplace Wood Texts
FIREPLACE_WOOD_COME_UP_DOWN_TEXT = 'Вы подошли к камину, который не горит.'
FIREPLACE_WOOD_COME_UP_LOWERED_TEXT = 'Вы подошли к камину, который каким-то образом потух.'
FIREPLACE_WOOD_COME_UP_RAISED_TEXT = 'Вы подошли к камину, который каким-то макаром зажогся.'
FIREPLACE_WOOD_COME_UP_UP_TEXT = 'Вы подошли к камину, который горит.'
FIREPLACE_WOOD_COME_UP_UNKNOWN_TEXT = 'Вы подошли к камину, с которым фиг знает что.'
FIREPLACE_WOOD_TOP_TEXT_WET = 'Вы подошли к камину и дрова в нем мокрые.'

FIREPLACE_WOOD_RESET_EFFECT_TEXT = 'Заменить намокшие дрова на сухие, которые как раз лежат рядом'
FIREPLACE_WOOD_RESET_EFFECT_RESULT_TEXT = 'Вы взяли сухие дрова, а на их место положили мокрые, ' \
                                     'через время они сами высохнут.',
FIREPLACE_WOOD_BLOW_OUT_TEXT = 'Потушить дрова в камине крышкой от унитаза.',
FIREPLACE_WOOD_BLOW_OUT_RESULT_TEXT = 'Вы потушили камин.'
FIREPLACE_WOOD_BLOW_OUT_WITH_SNOW_TEXT = 'Потушить дрова снегом.'
FIREPLACE_WOOD_BLOW_OUT_WITH_SNOW_RESULT_TEXT = 'Вы потушили дрова снегом.'
FIREPLACE_WOOD_BLOW_OUT_WITH_WATER_TEXT = 'Потушить дрова водой из ведра.'
FIREPLACE_WOOD_BLOW_OUT_WITH_WATER_RESULT_TEXT = 'Вы потушили дрова водой.'
FIREPLACE_WOOD_LIGHT_UP_TEXT = 'Зажечь камин огнивом.'
FIREPLACE_WOOD_LIGHT_UP_RESULT_TEXT = 'Вы зажгли дрова в камине.'
FIREPLACE_WOOD_WET_TEXT = 'Намочить дрова в камине.'
FIREPLACE_WOOD_WET_RESULT_TEXT = 'Вы намочили дрова в камине.'
