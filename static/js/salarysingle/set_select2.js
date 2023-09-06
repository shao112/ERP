var salaryDetails = [
  { name: "基本薪資", deduction: false },
  { name: "職務加給", deduction: false },
  { name: "手機加給", deduction: false },
  { name: "證照加給", deduction: false },
  { name: "伙食加給", deduction: false },
  { name: "出差加給", deduction: false },
  { name: "生活津貼", deduction: false },
  { name: "員工子女育兒津貼", deduction: false },
  { name: "車輛管理員津貼", deduction: false },
  { name: "E點出差加給", deduction: false },
  { name: "車程加給", deduction: false },
  { name: "其他津貼", deduction: false },
  { name: "值班加給", deduction: false },
  { name: "年終獎金", deduction: false },
  { name: "勞動節獎金", deduction: false },
  { name: "端午節獎金", deduction: false },
  { name: "中秋節獎金", deduction: false },
  { name: "歲修獎金", deduction: false },
  { name: "其他免稅加項", deduction: false },
  { name: "其他應稅加項", deduction: false },
  { name: "特休未休代金", deduction: false },
  { name: "勞健保溢收退回", deduction: false },
  { name: "績效獎金", deduction: false },
  { name: "免稅加班", deduction: false },
  { name: "工作津貼", deduction: false },
  // 扣款項
  { name: "勞保費", deduction: true },
  { name: "健保費", deduction: true },
  { name: "勞退自提", deduction: true },
  { name: "事假", deduction: true },
  { name: "病假", deduction: true },
  { name: "生理假", deduction: true },
  { name: "家庭照顧假", deduction: true },
  { name: "無薪假", deduction: true },
  { name: "曠職", deduction: true },
  { name: "代扣補充保費", deduction: true },
  { name: "其他免稅扣項", deduction: true },
  { name: "其他應稅扣項", deduction: true },
  { name: "勞健保短收補扣", deduction: true },
  { name: "代扣訂餐費", deduction: true },
  { name: "颱風假", deduction: true },
];

const selectElement = $("#salary-details-select");

const addGroup = selectElement.find("optgroup[label='加項']");
const deductGroup = selectElement.find("optgroup[label='扣項']");
salaryDetails.forEach((item) => {
  const option = document.createElement("option");
  option.text = item.name;
  option.value = item.name;
  if (item.deduction) {
    deductGroup.append(option);
  } else {
    addGroup.append(option);
  }
});

selectElement.select2({
  tags: true,
});
