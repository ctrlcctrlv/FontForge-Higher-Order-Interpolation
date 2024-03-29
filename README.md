# Higher-order interpolation, a.k.a. non-linear interpolation, in FontForge

![](https://raw.githubusercontent.com/ctrlcctrlv/FontForge-Higher-Order-Interpolation/main/dist/FontForgeHOI.gif)

> Mathematics belongs to God. ~ Donald Knuth

Higher-order interpolation is a concept long thought to have benefits for type design, best explained by Underware in their April 2018 case study ["Higher Order Interpolation for Variable Fonts"](https://underware.nl/case-studies/hoi/). Credit is given to Underware for exciting users about the prospect of higher-order interpolation.

This is a software implementation of higher-order interpolation using only free software: FontForge, fontmake, and the Python scripts in this repository. The implementors of HarfBuzz, for example, already knew that such higher-order implementation was in theory possible, and made their software correctly understand fonts with linked axes for the purpose of implementing them.

Please see the [companion YouTube video](https://www.youtube.com/watch?v=m5z4sDECCGA) for more.

# How this works

In a nutshell, `build.sh` does the following:

* Uses the FontForge API to generate four UFO masters: A, B, C, and D;
  * The A master is the position of all points at the beginning of the animation (axis value = 0). The B master is the position of the points offset by the first control point of the «HOI paths» layer spline for that point. Ditto for C, just with second control point. The D master is the position of all points at the end of the animation (axis value = 1000).
* Run fontmake to combine those four masters using a specially designed `designspace` file.
* Run my own script, which uses `fonttools.ttLib`, to “mangle” the output font. By this I mean, rename the axes in `fvar` and `STAT` so that all three axes appear to downstream software as one. Kudos to Dave Crossland for this idea.

# Dependencies

* FontForge
* `fontmake`
* Python library `fonttools`
* harfbuzz

As in all my fonts, only free software is used.

# UI tool

To receive the «Higher-Order Interpolation» item in the FontForge «Tools» menu, add `FF_HOI_UI.py` and the `lib/` directory to your FontForge Python directory. On my system, that is `~/.config/fontforge/python/`.

# Changing glyph metrics along axis

You can change the glyph metrics at different states of the animation by adding a special comment to your glyph. See an example in the `period` glyph:

```json
!!FRB FF HOIINFO v0
{
  "c1_rbearing": 550,
  "c2_rbearing": 550,
  "c3_rbearing": 750
}
```

* `c1` = master A
* `c2` = master B
* `c3` = master C
* rbearing in SFD file = master D

# License

This font editor implementation of higher-order interpolation (every file in this repository) is licensed under the Apache License v2.0.

You may not use these files except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

