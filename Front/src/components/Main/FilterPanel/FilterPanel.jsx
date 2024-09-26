import FilterByCatalog from "./FilterByCatalog/FilterByCatalog.jsx";
import FilterByUser from "./FilterByUser/FilterByUser.jsx";
import FilterByString from "./FilterByString/FilterByString.jsx";

import "./FilterPanel.css";

const FilterPanel = ({ filter, setFilter }) => {
  return (
    <div className="filter-panel">
      <FilterByCatalog caption="Модель техники" category="tec" store={filter} changer={setFilter} visible={"tec" in filter} />
      <FilterByCatalog caption="Модель двигателя" category="eng" store={filter} changer={setFilter} visible={"eng" in filter} />
      <FilterByCatalog caption="Модель трансмиссии" category="trm" store={filter} changer={setFilter} visible={"trm" in filter} />
      <FilterByCatalog caption="Модель ведущего моста" category="lda" store={filter} changer={setFilter} visible={"lda" in filter} />
      <FilterByCatalog caption="Модель управляемого моста" category="sta" store={filter} changer={setFilter} visible={"sta" in filter} />
      <FilterByCatalog caption="Вид ТО" category="man" store={filter} changer={setFilter} visible={"man" in filter} />
      <FilterByCatalog caption="Узел отказа" category="mfn" store={filter} changer={setFilter} visible={"mfn" in filter} />
      <FilterByCatalog caption="Способ восстановления" category="rec" store={filter} changer={setFilter} visible={"rec" in filter} />
      <FilterByUser caption="Клиент" category="c" store={filter} changer={setFilter} visible={"c" in filter} />
      <FilterByUser caption="Сервисная  компания" category="s" store={filter} changer={setFilter} visible={"s" in filter} />
      <FilterByString caption="Заводской номер" category="serial" store={filter} changer={setFilter} visible={"ser" in filter} />
    </div>
  );
};

export default FilterPanel;
