/* Demo code for serial communication
 * Sends an 'X' character when button pressed
 * Listens for 'L' and then toggles LED
 * Simple polled-serial style
 * */

#include <avr/io.h>
#include <avr/power.h>
#include <util/delay.h>

// These definitions make manipulating bits more readable 
#define BV(bit)               (1 << bit)
#define set_bit(byte, bit)    (byte |= BV(bit))  // old sbi()
#define clear_bit(byte, bit)  (byte &= ~BV(bit)) // old cbi()
#define toggle_bit(byte, bit) (byte ^= BV(bit))

#define LED                     PB0
#define LED_PORT                PORTB
#define LED_DDR                 DDRB

#define BUTTON                  PB1
#define BUTTON_PORT             PORTB
#define BUTTON_PIN              PINB

int main(void) {

    clock_prescale_set(clock_div_1);               /* CPU Clock: 8 MHz */

    // Initialize serial
    UBRR0 = 12;                            /* (8 MHz / 16 / 38400) - 1 */
    set_bit(UCSR0B, RXEN0);                               /* enable RX */
    set_bit(UCSR0B, TXEN0);                               /* enable TX */

    // Initialize input/output
    set_bit(BUTTON_PORT, BUTTON);      /* set internal pullup resistor */
    set_bit(LED_DDR, LED);                  /* set output mode for LED */

    while (1) {

        // Poll to see if serial has a byte
        if (bit_is_set(UCSR0A, RXC0)){
            if (UDR0 == 'L'){        /* if the received byte is an 'L' */
                toggle_bit(LED_PORT, LED);                /* blink LED */
            }
        }

        // Check to see if button pressed
        // button wired to ground, so a low voltage is a press 
        if (bit_is_clear(BUTTON_PIN, BUTTON)){
                                      /* wait for send buffer to clear */
            loop_until_bit_is_set(UCSR0A, UDRE0);
            UDR0 = 'X';                     /* load up data to be sent */
                  /* delay a second to keep from opening too many tabs */
            _delay_ms(1000);
        }

    }                                                /* End event loop */
    return 0;    
}
