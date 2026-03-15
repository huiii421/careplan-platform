# Product Requirements Document (PRD) / 产品需求文档

## 1. Document Info / 文档信息

- Product Name / 产品名称: Care Plan Auto-Generation Platform / 护理计划自动生成平台
- Customer / 客户: Specialty Pharmacy / 专科药房
- Version / 版本: v1.0
- Date / 日期: 2026-03-16
- Owner / 负责人: Product + Engineering Team / 产品与研发团队

## 2. Background and Problem / 背景与问题

### English
Pharmacists currently spend 20-40 minutes per patient manually creating care plans from patient records. This causes operational backlog, compliance risk, and reimbursement delay (Medicare and pharmaceutical programs), especially under severe staffing shortages.

### 中文
当前药师需要为每位患者手工整理护理计划，耗时约 20-40 分钟。由于人手紧张，这导致任务积压、合规风险上升，并影响 Medicare 及药企项目的报销效率。

## 3. Goals / 产品目标

### English
1. Reduce pharmacist documentation time per patient from 20-40 minutes to under 5 minutes assisted workflow.
2. Ensure data quality and consistency through strict validation and integrity rules.
3. Automatically generate downloadable care plans using an LLM.
4. Support quick reporting export for pharmaceutical partners and compliance audits.

### 中文
1. 将单患者护理计划制作时间从 20-40 分钟降低到 5 分钟以内（辅助式流程）。
2. 通过严格校验与一致性规则确保数据质量。
3. 调用 LLM 自动生成可下载的护理计划文本。
4. 支持面向药企与合规审计的快速报表导出。

## 4. Non-Goals (Phase 1) / 非目标（第一期）

### English
1. Not replacing pharmacist clinical judgment.
2. Not integrating directly with every external EHR in phase 1.
3. Not providing medical billing claim submission in phase 1.

### 中文
1. 不替代药师临床判断。
2. 第一期不对接所有外部 EHR 系统。
3. 第一期不包含医保/保险理赔提交功能。

## 5. Users and Roles / 用户与角色

### English
1. Medical Assistant: enters patient/order/provider data, uploads records, triggers generation.
2. Pharmacist: reviews generated care plan, edits/approves, finalizes.
3. Admin/Compliance: manages reference data, exports reports, audits logs.

### 中文
1. 医疗助理：录入患者/处方/医生信息，上传记录，触发生成。
2. 药师：审核并修订自动生成结果，确认发布。
3. 管理/合规人员：管理基础数据、导出报表、审计日志。

## 6. Scope and Core Workflow / 范围与核心流程

### English
1. Create patient case from validated web form.
2. Detect potential duplicates (patient and order).
3. Persist provider once and reuse by NPI.
4. Call LLM with structured clinical context.
5. Return care plan draft, allow review and download.
6. Export report-friendly records (CSV/XLSX).

### 中文
1. 通过带校验的 Web 表单创建患者案例。
2. 检测潜在重复（患者重复、医嘱重复）。
3. 医生按 NPI 唯一存储并复用。
4. 用结构化临床信息调用 LLM。
5. 返回护理计划草稿，支持审核与下载。
6. 支持报表导出（CSV/XLSX）。

## 7. Functional Requirements / 功能需求

### FR-1 Patient & Case Intake Form / 患者与案例录入表单

Required inputs / 必填输入:
1. Patient First Name (string) / 名
2. Patient Last Name (string) / 姓
3. Referring Provider (string) / 转诊医生姓名
4. Referring Provider NPI (10 digits) / 转诊医生 NPI（10 位数字）
5. Patient MRN (unique identifier) / 患者 MRN（唯一标识）
6. Primary Diagnosis (ICD-10) / 主诊断（ICD-10）
7. Medication Name (string) / 药品名称
8. Additional Diagnoses (list of ICD-10) / 附加诊断（ICD-10 列表）
9. Medication History (list of strings) / 用药史（字符串列表）
10. Patient Records (text and/or PDF) / 病历文本或 PDF

### FR-2 Validation Engine / 校验引擎

### English
1. Required-field validation with clear inline messages.
2. Format validation:
   - NPI: exactly 10 numeric digits.
   - ICD-10: valid code pattern and known-code check (if dictionary available).
   - MRN: configurable pattern (default 6-8 digits due to sample mismatch).
3. File upload validation for PDF/text type and max size.
4. Cross-field checks (for example, at least one diagnosis and one medication present).

### 中文
1. 所有必填项需实时校验并显示明确错误提示。
2. 格式校验：
   - NPI：必须为 10 位数字。
   - ICD-10：符合编码格式，并在可用字典时进行合法性校验。
   - MRN：可配置位数规则（默认 6-8 位，兼容示例与描述差异）。
3. 上传文件类型与大小校验（PDF/文本）。
4. 跨字段一致性校验（如至少一项诊断与一项用药）。

### FR-3 Duplicate Detection / 重复识别

### English
1. Warn if patient likely duplicate using MRN exact match or high-confidence demographic match.
2. Warn if order likely duplicate based on patient + diagnosis + medication + recent date window.
3. Warning is non-destructive; user may continue with explicit confirmation.

### 中文
1. 患者重复预警：MRN 精确匹配或高置信度人口学匹配。
2. 医嘱重复预警：基于患者 + 诊断 + 药品 + 时间窗口判断。
3. 预警为非阻断式，需用户确认后可继续。

### FR-4 Provider Mastering / 医生主数据唯一化

### English
1. Provider records must be unique by NPI.
2. If existing NPI is found, reuse existing provider record.
3. Prevent duplicate provider creation with transaction-safe constraints.

### 中文
1. 医生记录按 NPI 唯一。
2. 若 NPI 已存在，自动复用已有医生档案。
3. 通过事务与唯一约束避免并发重复创建。

### FR-5 LLM Care Plan Generation / LLM 护理计划生成

### English
1. Generate care plan draft from structured inputs and patient records.
2. Output must include:
   - Problem list / DTPs
   - SMART goals
   - Pharmacist interventions
   - Monitoring and lab schedule
3. Save prompt, model metadata, and output version for auditability.
4. Allow pharmacist edits before finalization.

### 中文
1. 基于结构化输入与病历内容生成护理计划草稿。
2. 输出至少包含：
   - 问题清单 / 药物治疗问题
   - SMART 目标
   - 药师干预方案
   - 监测与检验计划
3. 保存提示词、模型元数据与输出版本，满足审计要求。
4. 支持药师审核编辑后再定稿。

### FR-6 Download and Reporting Export / 下载与报表导出

### English
1. Download finalized care plan as TXT (phase 1) and optional PDF (phase 2).
2. Export case summary and key fields to CSV/XLSX for reporting.
3. Export filter by date range, provider, diagnosis, and status.

### 中文
1. 定稿护理计划支持 TXT 下载（一期），PDF 可作为二期。
2. 案例摘要与关键字段支持 CSV/XLSX 导出。
3. 导出支持按时间、医生、诊断、状态筛选。

## 8. Data Model and Integrity Rules / 数据模型与一致性规则

### English
1. Patient:
   - Unique key: MRN
   - Required: first_name, last_name, DOB (if collected), sex (if collected)
2. Provider:
   - Unique key: NPI
3. Case/Order:
   - References Patient + Provider
   - Stores primary diagnosis, secondary diagnoses, medication, medication history
4. CarePlan:
   - One or more versions per case
   - Tracks status: draft, pharmacist_reviewed, finalized

### 中文
1. 患者实体：
   - 唯一键：MRN
   - 必填：姓名；若采集则 DOB/性别也应规范化
2. 医生实体：
   - 唯一键：NPI
3. 案例/医嘱实体：
   - 关联患者与医生
   - 存储主诊断、附加诊断、药物与用药史
4. 护理计划实体：
   - 同一案例可多版本
   - 状态流转：草稿 -> 药师审核 -> 定稿

## 9. Error Handling and Safety / 错误处理与安全性

### English
1. User-facing errors must be clear, non-technical, and actionable.
2. LLM/API failures must not lose user-entered data.
3. Sensitive data must be masked in logs.
4. All critical operations should be traceable through audit logs.

### 中文
1. 面向用户的错误提示必须清晰、可执行、非技术化。
2. LLM/API 失败时不得丢失已录入数据。
3. 日志中对敏感信息做脱敏处理。
4. 关键操作需具备可追溯审计日志。

## 10. Non-Functional Requirements / 非功能需求

### English
1. Reliability: graceful handling of external model timeouts/retries.
2. Performance:
   - Form save: p95 < 1 second
   - Care plan generation: target < 30 seconds (async allowed)
3. Maintainability: modular code with separated validation/domain/integration layers.
4. Deployability: project runs out-of-box via documented setup.

### 中文
1. 可靠性：外部模型超时与重试要可控且可恢复。
2. 性能：
   - 表单保存 p95 小于 1 秒
   - 护理计划生成目标小于 30 秒（可异步）
3. 可维护性：校验层、领域层、集成层分离。
4. 可部署性：按文档可一键启动并端到端运行。

## 11. Testing Requirements / 测试要求

### English
1. Unit tests:
   - Field validators (NPI, ICD-10, MRN)
   - Duplicate detection rules
   - Provider uniqueness logic
2. Integration tests:
   - End-to-end form submit -> generate -> download
   - Error cases for invalid inputs and LLM failure fallback
3. Regression tests for core compliance fields and exports.

### 中文
1. 单元测试：
   - 字段校验（NPI、ICD-10、MRN）
   - 重复识别规则
   - 医生唯一化逻辑
2. 集成测试：
   - 端到端：录入 -> 生成 -> 下载
   - 异常路径：非法输入、LLM 失败回退
3. 回归测试：合规关键字段与导出结果。

## 12. Acceptance Criteria / 验收标准

### English
1. All required fields are validated both client-side and server-side.
2. Duplicate warnings appear in expected scenarios.
3. Provider cannot be duplicated by same NPI.
4. Care plan can be generated, reviewed, and downloaded for valid input.
5. Reporting export includes required compliance fields.
6. Automated tests cover critical logic and pass in CI.

### 中文
1. 所有必填与关键格式项均实现前后端双重校验。
2. 预期场景下可触发患者/医嘱重复预警。
3. 相同 NPI 不可重复创建医生。
4. 合法输入可完成“生成-审核-下载”闭环。
5. 报表导出包含合规所需字段。
6. 关键逻辑有自动化测试并在 CI 通过。

## 13. Example Clinical Input Mapping / 示例临床输入映射

### English
The provided fictional patient sample (A.B., MRN 00012345, IVIG use case for generalized myasthenia gravis) should generate a care plan containing:
1. Clinical rationale for rapid immunomodulation.
2. Safety controls for infusion reactions, renal function, and thromboembolic risk.
3. SMART goals and measurable timeline (2 weeks).
4. Monitoring plan: baseline CBC/BMP/vitals, infusion vitals q15-30 min, post-course BMP in 3-7 days.

### 中文
给定虚构患者示例（A.B.，MRN 00012345，IVIG 用于全身型重症肌无力）应产出护理计划，至少覆盖：
1. 需要快速免疫调节的临床依据。
2. 输注反应、肾功能、血栓风险的安全控制。
3. SMART 目标及 2 周评估时间点。
4. 监测计划：治疗前 CBC/BMP/生命体征，输注中 q15-30 分钟监测，疗程后 3-7 天复查 BMP。

## 14. Open Decisions / 待确认项

### English
1. Final MRN rule: exactly 6 digits or variable length (6-8) for legacy compatibility.
2. ICD-10 source of truth: static dictionary, external API, or both.
3. Export format priority: CSV only in phase 1 vs CSV + XLSX.
4. Whether DOB/sex are mandatory in MVP intake form.

### 中文
1. MRN 最终规则：固定 6 位，还是兼容历史数据（6-8 位）。
2. ICD-10 数据源：内置字典、外部 API，还是双轨。
3. 一期导出优先级：仅 CSV 或同时支持 XLSX。
4. MVP 阶段 DOB/性别是否设为必填。

