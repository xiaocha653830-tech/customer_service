-- SET NAMES utf8mb4;

-- CREATE DATABASE IF NOT EXISTS `customer_service`
--   DEFAULT CHARACTER SET utf8mb4
--   DEFAULT COLLATE utf8mb4_unicode_ci;

-- GRANT ALL PRIVILEGES ON `customer_service`.* TO 'atguigu'@'%';
-- FLUSH PRIVILEGES;

USE `customer_service`;

CREATE TABLE IF NOT EXISTS `dialogue_states` (
  `sender_id` VARCHAR(255) NOT NULL COMMENT '用户唯一标识',
  `state_json` TEXT NOT NULL COMMENT '完整对话状态 JSON',
  PRIMARY KEY (`sender_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

USE `customer_service`;

-- 样本1：u1001（活跃状态，包含任务、焦点对象、历史会话与待处理轮次）
INSERT INTO `dialogue_states` (`sender_id`, `state_json`) VALUES
(
  'u1001', 
  '{
    "sender_id": "u1001", 
    "active_task": {
          "task_id": "T1001",
          "task_type": "refund", 
          "status": "processing"
                   }, 
    "paused_tasks": [
      {
          "task_id": "T0999", 
          "task_type": "shipping_urge", 
          "status": "paused"
      }
                    ], 
    "active_system_task": null, 
    "focused_object": {
          "type": "order", 
          "id": "A20260410001", 
          "title": "订单 A20260410001", 
          "attributes": {
                  "status": "待发货", 
                  "amount": 8999.0
                        }}, 
    "sessions": [
        {
          "session_id": "S20260410001", 
          "created_at": 1712707200.0, 
          "last_activity_at": 1712710800.0, 
          "closed_at": 1712714400.0, 
          "turns": [{
                  "turn_id": "turn_1", 
                  "input_message": {"role": "user","content": "我的订单什么时候发货？"}, 
                  "assistant_message": [{"role": "bot","content": "您好,您的订单正在备货中,预计24小时内发出。"}]
                   }]
        }
                ], 
    "current_session_id": "S20260410001" 
  }'
),
-- 样本2：u1002（仅包含系统任务和焦点对象，无历史会话）
(
  'u1002', 
  '{"sender_id": "u1002", "active_task": null, "paused_tasks": [], "active_system_task": {"task_id": "SYS_001", "task_type": "logistics_query", "status": "completed"}, "focused_object": {"type": "product", "id": "SKU10006", "title": "罗技 MX Master 3S 鼠标", "attributes": {"price": 699.0}}, "sessions": [], "current_session_id": null}'
),
-- 样本3：u1003（全新用户，空状态）
(
  'u1003', 
  '{"sender_id": "u1003", "active_task": null, "paused_tasks": [], "active_system_task": null, "focused_object": null, "sessions": [], "current_session_id": null}'
);

-- 验证插入结果
SELECT * FROM `dialogue_states`;

