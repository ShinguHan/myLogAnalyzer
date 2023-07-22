sequenceDiagram
participant cv as CNV
participant mc as MCS
autonumber

    note over cv,mc : Diverter 상태 변경 보고
    cv ->> mc : S6F11 - DiverterInService (CEID = 305)<br>SubState (1 - RUN)
    mc ->> cv : S6F12

    note over cv, mc : Report ID Read
    cv ->> mc : S6F11 - ReportIDRead (CEID = 643)
    mc ->> cv : S6F12 - ERA (Event Report Ack)

    note over cv, mc : Carrier ID Read
    cv ->> mc : S6F11 - Carrier ID Read (CEID = 251)
    mc ->> cv : S6F12 - IDReadStatus = 0

    note over cv, mc : CNV 동작
    cv ->> mc : S6F11 - CarrierWaitIn (CEID = 158)
    mc ->> cv : S6F12 - ERA

    note over cv, mc : Transfer 지시
    mc ->> cv : S2F49 - Enhanced Remote Command(ERC)
    cv ->> mc : S2F50 - HCACK (ERCA)

    note over cv, mc : 반송 명령 초기화
    cv ->> mc : S6F11 - TransferInitiated (CEID = 108)
    mc ->> cv : S6F12 - ERA

    note over cv, mc : Carrier 위치 이동
    cv ->> mc : S6F11 - CarrierTransferring (CEID = 157)
    mc ->> cv : S6F12 - ERA

    cv ->> mc : S6F11 - CarrierBeltTransferring (CEID = 607)
    mc ->> cv : S6F12 - ERA

    cv ->> mc : S6F11 - BeltInService (CEID = 307)
    cv ->> mc : subState = 1(RUN)
    mc ->> cv : S6F12 - ERA

    cv ->> mc : S6F11 - DiverterInService (CEID = 305)
    cv ->> mc : SubState (2 - IDLE)
    mc ->> cv : S6F12 - ERA

    cv ->> mc : S6F11 - BeltInService (CEID = 307)
    cv ->> mc : subState = 2(RUN)
    mc ->> cv : S6F12 - ERA

    cv ->> mc : S6F11 - DiverterInService (CEID = 305)
    cv ->> mc : SubState (1 - RUN)
    mc ->> cv : S6F12 - ERA

    note over cv,mc : CNV 출고 Port 도착
    cv ->> mc : S6F11 - CarrierWaitOUt (CEID = 159)
    mc ->> cv : S6F12 - ERA

    note over cv,mc : 동작 완료
    cv ->> mc : S6F11 - TransferCompleted (CEID = 107)
    mc ->> cv : S6F12 - ERA

    note over cv,mc : Carrier Removed
    cv ->> mc : S6F11 - CarrierRemoved (CEID = 153)
    mc ->> cv : S6F12 - ERA
