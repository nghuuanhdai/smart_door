#ifndef __TIMER.H
#define __TIMER.H

void init_timer_interrupt(void);
void init_timer_software(void);
void setTimer(int, int);
int getTimerFlag(int);
void resetTimer(int);
void timer_run(void);

#endif
