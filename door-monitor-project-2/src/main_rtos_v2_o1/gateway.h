#ifndef __GATEWAY.H
#define __GATEWAY.H

void init_gateway();
void gateway_command_received_parse();
String task_gateway_sending_outroom(String IDs);
String task_gateway_sending_inroom(String IDs, float temperature);
String task_gateway_toggle_LED(int level);
String task_gateway_count_people();
String task_gateway_message_timeout(String id);
String task_gateway_sending_remove_timeout(String id);
#endif
